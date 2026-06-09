from __future__ import annotations

import asyncio
import json
import unittest
from typing import Any, Dict, Tuple

try:
    from scsp_viz.web_api import app
except ModuleNotFoundError as exc:  # pragma: no cover - dependency bootstrap path
    raise unittest.SkipTest("fastapi is not installed") from exc


METRIC_FIELDS = {
    "total_samples",
    "total_latency_s",
    "data_tx_latency_s",
    "inter_stage_latency_s",
    "stage1_compute_latency_s",
    "stage2_compute_latency_s",
    "effective_compute_flops",
    "effective_compute_pflops",
    "ideal_peak_pflops",
    "compute_utilization",
    "bottleneck_stage",
    "decode_latency_s_per_token",
    "decode_total_latency_s",
    "decode_compute_latency_s_per_token",
    "decode_memory_latency_s_per_token",
    "decode_effective_compute_pflops",
    "decode_bottleneck",
    "prefill_compute_time_s",
    "prefill_memory_time_s",
    "prefill_time_s",
    "prefill_bottleneck",
    "decode_energy_efficiency_tokens_per_j",
    "total_inference_time_s",
    "prefill_peak_memory_bytes",
    "prefill_peak_memory_gb",
    "single_star_peak_memory_bytes",
    "single_star_peak_memory_gb",
    "prefill_weight_memory_bytes",
    "prefill_kv_memory_bytes",
    "prefill_activation_peak_memory_bytes",
    "prefill_workspace_memory_bytes",
}


def _request(method: str, path: str, json_body: Dict[str, Any] | None = None) -> Tuple[int, Dict[str, Any]]:
    async def run() -> Tuple[int, Dict[str, Any]]:
        body = b"" if json_body is None else json.dumps(json_body).encode("utf-8")
        messages = [{"type": "http.request", "body": body, "more_body": False}]
        sent = []

        async def receive() -> Dict[str, Any]:
            return messages.pop(0)

        async def send(message: Dict[str, Any]) -> None:
            sent.append(message)

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": method,
            "scheme": "http",
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "headers": [(b"host", b"testserver"), (b"content-type", b"application/json")],
            "client": ("127.0.0.1", 1234),
            "server": ("testserver", 80),
        }
        await app(scope, receive, send)
        status = next(message["status"] for message in sent if message["type"] == "http.response.start")
        response_body = b"".join(message.get("body", b"") for message in sent if message["type"] == "http.response.body")
        return status, json.loads(response_body.decode("utf-8"))

    return asyncio.run(run())


def test_health_endpoint() -> None:
    status, payload = _request("GET", "/api/health")

    assert status == 200
    assert payload == {"status": "ok"}


def test_single_simulation_api_returns_full_mock_metrics() -> None:
    status, payload = _request(
        "POST",
        "/api/simulations/single",
        {"config": {"link_bandwidth_gbps": 100}, "bandwidth_gbps": 100},
    )

    assert status == 200
    assert payload["mode"] == "single"
    assert METRIC_FIELDS <= set(payload["metrics"])
    assert payload["config"]["link_bandwidth_gbps"] == 100.0


def test_sweep_simulation_api_returns_required_rows() -> None:
    status, payload = _request(
        "POST",
        "/api/simulations/sweep",
        {"config": {"link_bandwidth_gbps": [10, 100]}, "bandwidths_gbps": [10, 100]},
    )

    assert status == 200
    assert payload["mode"] == "sweep"
    assert payload["knee_reason"]
    assert len(payload["rows"]) == 2
    assert {
        "link_bandwidth_gbps",
        "total_latency_s",
        "effective_compute_pflops",
        "bottleneck_stage",
        "decode_latency_s_per_token",
        "decode_total_latency_s",
        "decode_effective_compute_pflops",
        "decode_energy_efficiency_tokens_per_j",
        "decode_bottleneck",
    } <= set(payload["rows"][0])
