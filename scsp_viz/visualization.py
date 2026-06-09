from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence


def _coerce_number(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return float(value) if "." in value else int(value)
        except ValueError:
            return value
    return value


def _load_sweep_rows(source: Sequence[Dict[str, Any]] | str | Path) -> List[Dict[str, Any]]:
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Sweep result file not found: {path}")
        suffix = path.suffix.lower()
        if suffix == ".csv":
            with path.open("r", encoding="utf-8", newline="") as f:
                return [{k: _coerce_number(v) for k, v in row.items()} for row in csv.DictReader(f)]
        if suffix == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and "rows" in payload:
                return list(payload["rows"])
            if isinstance(payload, list):
                return payload
            raise ValueError("JSON sweep result must be a list or an object containing rows")
        raise ValueError("Sweep result file must be CSV or JSON")
    return [dict(row) for row in source]


def plot_sweep_latency(rows: List[Dict[str, Any]] | str | Path, output_prefix: str, model_name: str) -> str:
    output_dir = Path(output_prefix)
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_path = output_dir / "sweep_latency_vs_bandwidth.png"

    sweep_rows = _load_sweep_rows(rows)
    if not sweep_rows:
        raise ValueError("Sweep result rows cannot be empty")
    sorted_rows = sorted(sweep_rows, key=lambda x: x["link_bandwidth_gbps"])
    x = [row["link_bandwidth_gbps"] for row in sorted_rows]
    y = [row["total_latency_s"] for row in sorted_rows]

    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o", linestyle="-", linewidth=2)
    plt.xlabel("Inter-satellite Link Bandwidth (Gbps)")
    plt.ylabel("Total Latency (s)")
    plt.title(model_name)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)
    plt.close()
    return str(plot_path)
