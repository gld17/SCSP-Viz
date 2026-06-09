from __future__ import annotations

from dataclasses import asdict
from numbers import Integral
from typing import Any, Dict, List

from .config import build_simulation_config, dump_config_dict, normalize_raw_config
from .models import SimulationMetrics


def validate_bandwidth_input(value: Any) -> None:
    if isinstance(value, Integral):
        if value <= 0:
            raise ValueError("link_bandwidth_gbps must be a positive integer")
        return
    if isinstance(value, list):
        if not value:
            raise ValueError("link_bandwidth_gbps list cannot be empty")
        for item in value:
            if not isinstance(item, Integral):
                raise TypeError("link_bandwidth_gbps list items must be integers")
            if item <= 0:
                raise ValueError("link_bandwidth_gbps list items must be positive integers")
        return
    raise TypeError("link_bandwidth_gbps must be an integer or a list of integers")


def _mock_metrics(config: Dict[str, Any], bandwidth_gbps: float) -> Dict[str, Any]:
    cfg = build_simulation_config(config, bandwidth_gbps)
    width, height = cfg.image_wh
    tile_w, tile_h = cfg.tile_wh
    pixels = width * height * max(cfg.num_images, 1)
    tile_pixels = max(tile_w * tile_h, 1)
    total_samples = max(1, int((pixels + tile_pixels - 1) // tile_pixels))
    bandwidth_factor = max(float(bandwidth_gbps), 1.0)
    compute_scale = max(cfg.big_star_peak_pflops * cfg.prefill_compute_utilization, 0.1)

    data_tx_latency_s = round((pixels * cfg.channels * cfg.bytes_per_pixel * 8) / (bandwidth_factor * 1e9), 6)
    inter_stage_latency_s = round(
        (cfg.prefill_inter_stage_transfer_mb * 8e6 + cfg.decode_inter_stage_transfer_kb * 8e3)
        / (bandwidth_factor * 1e9)
        + cfg.inter_sat_latency_target_ms / 1000.0,
        6,
    )
    stage1_compute_latency_s = round(total_samples * cfg.flops_per_sample / (compute_scale * 1e15), 6)
    stage2_compute_latency_s = round(stage1_compute_latency_s * (1.0 - cfg.stage_split_ratio + 0.5), 6)
    prefill_compute_time_s = round(stage1_compute_latency_s + stage2_compute_latency_s, 6)
    prefill_memory_time_s = round(total_samples * cfg.prefill_memory_bytes_per_patch / cfg.single_node_memory_bandwidth_bytes_per_sec, 6)
    prefill_time_s = round(max(prefill_compute_time_s, prefill_memory_time_s) + inter_stage_latency_s, 6)
    decode_compute_latency_s_per_token = round(
        cfg.decode_flops_per_token / max(cfg.big_star_peak_pflops * cfg.decode_compute_utilization * 1e15, 1.0),
        6,
    )
    decode_memory_latency_s_per_token = round(
        cfg.decode_memory_bytes_per_token / max(cfg.single_node_memory_bandwidth_bytes_per_sec * cfg.decode_memory_utilization, 1.0),
        6,
    )
    decode_latency_s_per_token = round(
        max(decode_compute_latency_s_per_token, decode_memory_latency_s_per_token)
        + cfg.decode_inter_stage_transfer_kb * 8e3 / (bandwidth_factor * 1e9),
        6,
    )
    decode_total_latency_s = round(decode_latency_s_per_token * cfg.decode_tokens, 6)
    total_latency_s = round(data_tx_latency_s + prefill_time_s + decode_total_latency_s, 6)
    effective_compute_flops = cfg.flops_per_sample * total_samples / max(total_latency_s, 1e-9)
    effective_compute_pflops = round(effective_compute_flops / 1e15, 6)
    decode_effective_compute_pflops = round(
        cfg.decode_flops_per_token / max(decode_latency_s_per_token, 1e-9) / 1e15,
        6,
    )
    ideal_peak_pflops = cfg.big_star_peak_pflops
    compute_utilization = round(min(effective_compute_pflops / max(ideal_peak_pflops, 1e-9), 1.0), 6)
    prefill_weight_memory_bytes = cfg.resident_parameter_count * cfg.bytes_per_pixel
    prefill_kv_memory_bytes = cfg.decode_tokens * cfg.llm_num_hidden_layers * cfg.llm_hidden_size * 2 * cfg.bytes_per_pixel
    prefill_activation_peak_memory_bytes = pixels * cfg.channels * cfg.bytes_per_pixel * 4
    prefill_workspace_memory_bytes = total_samples * cfg.prefill_memory_bytes_per_patch * 0.05
    prefill_peak_memory_bytes = (
        prefill_weight_memory_bytes
        + prefill_kv_memory_bytes
        + prefill_activation_peak_memory_bytes
        + prefill_workspace_memory_bytes
    )
    single_star_peak_memory_bytes = min(prefill_peak_memory_bytes, cfg.peak_vram_gb * 1e9)

    metrics = SimulationMetrics(
        total_samples=total_samples,
        total_latency_s=total_latency_s,
        data_tx_latency_s=data_tx_latency_s,
        inter_stage_latency_s=inter_stage_latency_s,
        stage1_compute_latency_s=stage1_compute_latency_s,
        stage2_compute_latency_s=stage2_compute_latency_s,
        effective_compute_flops=effective_compute_flops,
        effective_compute_pflops=effective_compute_pflops,
        ideal_peak_pflops=ideal_peak_pflops,
        compute_utilization=compute_utilization,
        bottleneck_stage="communication" if data_tx_latency_s + inter_stage_latency_s > prefill_compute_time_s else "compute",
        decode_latency_s_per_token=decode_latency_s_per_token,
        decode_total_latency_s=decode_total_latency_s,
        decode_compute_latency_s_per_token=decode_compute_latency_s_per_token,
        decode_memory_latency_s_per_token=decode_memory_latency_s_per_token,
        decode_effective_compute_pflops=decode_effective_compute_pflops,
        decode_bottleneck="memory" if decode_memory_latency_s_per_token > decode_compute_latency_s_per_token else "compute",
        prefill_compute_time_s=prefill_compute_time_s,
        prefill_memory_time_s=prefill_memory_time_s,
        prefill_time_s=prefill_time_s,
        prefill_bottleneck="memory" if prefill_memory_time_s > prefill_compute_time_s else "compute",
        decode_energy_efficiency_tokens_per_j=round(1.0 / max(cfg.single_star_compute_payload_power_w * decode_latency_s_per_token, 1e-9), 9),
        total_inference_time_s=total_latency_s,
        prefill_peak_memory_bytes=prefill_peak_memory_bytes,
        prefill_peak_memory_gb=round(prefill_peak_memory_bytes / 1e9, 6),
        single_star_peak_memory_bytes=single_star_peak_memory_bytes,
        single_star_peak_memory_gb=round(single_star_peak_memory_bytes / 1e9, 6),
        prefill_weight_memory_bytes=prefill_weight_memory_bytes,
        prefill_kv_memory_bytes=prefill_kv_memory_bytes,
        prefill_activation_peak_memory_bytes=prefill_activation_peak_memory_bytes,
        prefill_workspace_memory_bytes=prefill_workspace_memory_bytes,
    )
    return asdict(metrics)


def mock_run_simulation(config: Dict[str, Any], bandwidth_gbps: int | None = None) -> Dict[str, Any]:
    normalized = normalize_raw_config(config)
    raw_bw = normalized["link_bandwidth_gbps"]
    if bandwidth_gbps is None and isinstance(raw_bw, list):
        bw = int(raw_bw[0])
    else:
        bw = int(raw_bw) if bandwidth_gbps is None else int(bandwidth_gbps)
    validate_bandwidth_input(bw)
    cfg = build_simulation_config(normalized, bw)
    return {
        "mode": "single",
        "config": dump_config_dict(cfg),
        "metrics": _mock_metrics(normalized, bw),
    }


def mock_run_sweep(config: Dict[str, Any], bandwidths_gbps: List[int] | None = None) -> Dict[str, Any]:
    normalized = normalize_raw_config(config)
    if bandwidths_gbps is None:
        raw_bw = normalized.get("link_bandwidth_gbps", [10, 50, 100, 200, 400])
        bandwidths_gbps = [int(v) for v in raw_bw] if isinstance(raw_bw, list) else [int(raw_bw)]
    validate_bandwidth_input(bandwidths_gbps)
    rows = []
    for bw in bandwidths_gbps:
        metrics = _mock_metrics(normalized, float(bw))
        rows.append(
            {
                "link_bandwidth_gbps": int(bw),
                "total_latency_s": metrics["total_latency_s"],
                "effective_compute_pflops": metrics["effective_compute_pflops"],
                "bottleneck_stage": metrics["bottleneck_stage"],
                "decode_latency_s_per_token": metrics["decode_latency_s_per_token"],
                "decode_total_latency_s": metrics["decode_total_latency_s"],
                "decode_effective_compute_pflops": metrics["decode_effective_compute_pflops"],
                "decode_energy_efficiency_tokens_per_j": metrics["decode_energy_efficiency_tokens_per_j"],
                "decode_bottleneck": metrics["decode_bottleneck"],
            }
        )
    sorted_rows = sorted(rows, key=lambda row: row["link_bandwidth_gbps"])
    knee = sorted_rows[-1]["link_bandwidth_gbps"] if sorted_rows else None
    for prev, cur in zip(sorted_rows, sorted_rows[1:]):
        improvement = prev["total_latency_s"] - cur["total_latency_s"]
        if prev["total_latency_s"] and improvement / prev["total_latency_s"] < 0.05:
            knee = cur["link_bandwidth_gbps"]
            break
    return {
        "mode": "sweep",
        "knee_bandwidth_gbps": knee,
        "knee_reason": "mock latency improvement below 5% threshold",
        "rows": sorted_rows,
    }
