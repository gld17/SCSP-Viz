# 本轮实现内容

- 完成 SCSP-Viz 独立项目交付层整理，保留 `scsp_viz/` 包、`run_web.py`、`web/index.html`、`assets/earth-horizon-reference.png`、`configs/model_registry.json`、`experiments/records.jsonl` 和部分 `experiments/runs/` 示例数据。
- `run_web.py` 已指向 `uvicorn.run("scsp_viz.web_api:app", ...)`。
- `scsp_viz/web_api.py` 已切换到 Mock 数据层，单点、扫描、实验运行、实验复现接口不依赖 v0 真实仿真引擎。
- `scsp_viz/experiment.py` 保留 `JsonlExperimentStore`、`ExperimentRecord`、`apply_experiment_template`、`compare_result_summary`、`reproduce_experiment` 等接口，实验运行写入 Mock JSON/CSV 结果。
- 新增并完善 `scsp_viz/mock_engine.py`，提供 `mock_run_simulation(config, bandwidth_gbps)` 和 `mock_run_sweep(config, bandwidths_gbps)`。
- 单点 Mock 返回 `{"mode": "single", "config": ..., "metrics": ...}`，`metrics` 覆盖 v0 `SimulationMetrics` 全部字段。
- 扫描 Mock 返回 `{"mode": "sweep", "knee_bandwidth_gbps": ..., "knee_reason": ..., "rows": ...}`，`rows` 覆盖要求的 9 个字段。
- `scsp_viz/config.py` 保留配置模型、标准化、校验和导出接口，默认值改为独立硬编码，不运行期依赖 model registry 推导仿真参数。
- `scsp_viz/visualization.py` 保留 `plot_sweep_latency` 兼容签名，支持从 CSV/JSON 实验结果文件读取扫描数据后绘图。
- `requirements.txt` 已包含 `fastapi`、`uvicorn`、`pydantic`、`matplotlib`。
- `tests/test_web_api.py` 和 `tests/test_experiment.py` 已覆盖 Mock API 返回结构、实验记录写入和复现流程；API 测试直接调用 ASGI app，避免额外 TestClient 依赖。
- `README.md` 已用中文说明项目简介、功能特性、目录结构、安装依赖、启动方式、REST API、前端页面和许可证声明。

# AC 推进情况

- Step 1 到 Step 10 已完成。
- 引用检查已完成：`scsp_viz`、`run_web.py`、`web`、`tests`、`README.md` 中未发现旧 `from scsp.`、`import scsp.`、`scsp.web_api`、`from .engine` 或 `from .io_utils import write_json` 残留。
- 示例数据检查已完成：目标项目 `experiments/records.jsonl` 与 `experiments/runs/` 下已有示例运行配置和结果文件。
- 标准库 smoke test 已通过：直接调用 `mock_run_simulation`、`mock_run_sweep`、`run_experiment`，验证单点 metrics 字段、扫描 rows 和实验写入结构。
- 测试已通过：`uv run --with fastapi --with uvicorn --with pydantic --with matplotlib --with pytest python -m pytest tests/test_web_api.py tests/test_experiment.py -q`，结果 `4 passed in 0.42s`。
- FastAPI 启动验证已通过：`uv run --with fastapi --with uvicorn --with pydantic --with matplotlib uvicorn scsp_viz.web_api:app --host 0.0.0.0 --port 8000`，`GET /api/health` 返回 `{"status":"ok"}`，随后进程已停止。

# 遗留问题

- 系统默认 `/usr/bin/python3` 环境缺少 `pip`，且未预装 `fastapi`、`uvicorn`、`pytest` 等依赖；本轮使用 `uv run` 临时隔离环境完成测试与启动验证。
- 未执行任何 git 命令，未修改 SCSP_v0 原仓库文件。

# Goal Tracker 更新请求

- Round 0 Builder 实现建议标记为完成：独立项目结构、Mock 数据层、REST API、实验记录、可视化入口、README、requirements、测试与启动验证均已完成。

# Lesson Delta

- 在该环境执行 Python Web 项目验证时，优先使用可用的 `uv run` 创建临时依赖环境；系统 Python 不一定带 `pip`。
- 从 v0 提取交付层后，应固定执行旧包名与真实引擎耦合扫描，重点覆盖 `from scsp.`、`import scsp.`、`scsp.web_api`、`.engine` 和真实运行函数引用。
