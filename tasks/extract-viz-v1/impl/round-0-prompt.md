# Round 0 任务

## 强制执行规则
你必须遵守 pbr-codex-builder skill。若未加载该 skill，也必须遵守：
1. 你是唯一 Builder，只写代码。
2. 不做 review 判断。
3. 不执行任何 git 命令。
4. 完成后必须写入指定 summary 文件：/share/guolidong-nfs/SeeSpace/SCSP-Viz/tasks/extract-viz-v1/impl/round-0-summary.md

## 重要限制
- 不要执行 git 命令（git add / git commit / git push 等）。如果你需要重命名文件，请直接创建新文件并写入内容，然后删除旧文件。
- 所有文件操作通过 Hermes 工具完成，不直接输出代码到对话中。
- 每次修改文件后，检查是否有 include 路径、import 路径或其他引用需要同步更新。
- 修改前先在相关文件中搜索所有引用，确认修改的安全性。
- 不要修改 SCSP_v0 原仓库的任何文件。
- 项目目录已重命名为 SCSP-Viz（带连字符）。

## 项目目标
构建独立项目 `SCSP-Viz`（星座智算可视化分析软件 V1.0），从 SCSP_v0 提取可视化交付层。不执行实际仿真计算，通过 Mock 数据层保证前端展示。

## 工程步骤

### Step 1：复制基础文件
从 `/share/guolidong-nfs/SeeSpace/SCSP_v0/` 复制以下文件到 `/share/guolidong-nfs/SeeSpace/SCSP-Viz/` 的对应位置（保持目录结构）：

复制到 `scsp_viz/` 目录下（注意包名改为 scsp_viz）：
- `scsp/__init__.py` → `scsp_viz/__init__.py`
- `scsp/web_api.py` → `scsp_viz/web_api.py`
- `scsp/experiment.py` → `scsp_viz/experiment.py`
- `scsp/visualization.py` → `scsp_viz/visualization.py`
- `scsp/config.py` → `scsp_viz/config.py`
- `scsp/io_utils.py` → `scsp_viz/io_utils.py`
- `scsp/models.py` → `scsp_viz/models.py`

复制到根目录：
- `run_web.py` → `run_web.py`
- `web/index.html` → `web/index.html`
- `assets/earth-horizon-reference.png` → `assets/earth-horizon-reference.png`
- `configs/model_registry.json` → `configs/model_registry.json`

同时复制 `experiments/records.jsonl` 和 `experiments/runs/` 下的一些示例数据到 `experiments/`。

### Step 2：改造 import 路径
将所有文件中的 `from scsp.` 改为 `from scsp_viz.`，将所有 `import scsp.` 改为 `import scsp_viz.`。

### Step 3：移除仿真引擎耦合
在 `scsp_viz/web_api.py` 中：
- 删除 `from .engine import run_simulation, run_sweep`
- 删除 `from .experiment import ... run_experiment` 中的真实运行引用（保留 ExperimentRecord 和 JsonlExperimentStore）
- 在 API 处理函数中，将 `run_simulation`、`run_sweep`、`run_experiment`、`reproduce_experiment` 的调用替换为 Mock 数据生成器

在 `scsp_viz/experiment.py` 中：
- 删除 `from .engine import run_simulation, run_sweep, validate_bandwidth_input`
- 删除 `from .io_utils import write_json`
- 将 `run_experiment` 中的真实仿真调用替换为 Mock 数据生成
- 保留 `JsonlExperimentStore`、`ExperimentRecord`、`apply_experiment_template`、`compare_result_summary`、`reproduce_experiment` 的接口签名，但内部用 Mock 数据填充

创建 `scsp_viz/mock_engine.py`：
- 提供 `mock_run_simulation(config, bandwidth_gbps)` 和 `mock_run_sweep(config, bandwidths_gbps)` 函数
- 返回与 v0 真实仿真结果结构完全一致的 Mock 数据（参考 v0 中 `engine.py` 的返回值结构）
- 单点仿真返回：`{"mode": "single", "config": ..., "metrics": {...}}`
- 扫描仿真返回：`{"mode": "sweep", "knee_bandwidth_gbps": ..., "knee_reason": ..., "rows": [...]}`
- Mock metrics 需包含 v0 `SimulationMetrics` 的所有字段（参考 v0 `models.py` 中的 dataclass）

### Step 4：保留配置校验层
`scsp_viz/config.py`：
- 保留 `V1SimulationConfig`、`normalize_raw_config`、`validate_raw_config`、`dump_config_dict`
- 删除与仿真计算强耦合的默认值推导（如从 model_registry 推导模型参数等），改为直接硬编码合理的默认值
- 保留 `build_simulation_config` 的签名，用于前端配置展示和校验

### Step 5：改造可视化模块
`scsp_viz/visualization.py`：
- 保留 `plot_sweep_latency` 函数
- 输入改为从实验结果文件（CSV 或 JSON）读取，而非直接调用引擎
- 确保函数签名与 v0 兼容

### Step 6：更新启动脚本
`run_web.py`：
- 将 `uvicorn.run("scsp.web_api:app", ...)` 改为 `uvicorn.run("scsp_viz.web_api:app", ...)`

### Step 7：创建 requirements.txt
包含：
```
fastapi
uvicorn
pydantic
matplotlib
```

### Step 8：创建 tests/
创建 `tests/test_web_api.py` 和 `tests/test_experiment.py`，至少包含对 Mock API 的调用测试，确保返回结构正确。

### Step 9：编写 README.md
中文，包含：
- 项目简介：SCSP-Viz 星座智算可视化分析软件 V1.0
- 功能特性（≥6项）
- 目录结构说明
- 安装依赖步骤
- 启动方式：`python run_web.py`
- 接口说明（与 SCSP 仿真平台的标准化 REST API 交互规范）
- 前端页面说明
- 许可证声明

### Step 10：验证可运行
在终端中执行 `cd /share/guolidong-nfs/SeeSpace/SCSP-Viz && uvicorn scsp_viz.web_api:app --host 0.0.0.0 --port 8000 &` 或类似命令验证 FastAPI 可正常启动无报错（启动后立即停止即可，不需要保持运行）。

## Mock 数据结构要求
单点仿真 metrics 必须包含以下字段（与 v0 一致）：
```
total_samples, total_latency_s, data_tx_latency_s, inter_stage_latency_s,
stage1_compute_latency_s, stage2_compute_latency_s, effective_compute_flops,
effective_compute_pflops, ideal_peak_pflops, compute_utilization, bottleneck_stage,
decode_latency_s_per_token, decode_total_latency_s, decode_compute_latency_s_per_token,
decode_memory_latency_s_per_token, decode_effective_compute_pflops, decode_bottleneck,
prefill_compute_time_s, prefill_memory_time_s, prefill_time_s, prefill_bottleneck,
decode_energy_efficiency_tokens_per_j, total_inference_time_s,
prefill_peak_memory_bytes, prefill_peak_memory_gb, single_star_peak_memory_bytes,
single_star_peak_memory_gb, prefill_weight_memory_bytes, prefill_kv_memory_bytes,
prefill_activation_peak_memory_bytes, prefill_workspace_memory_bytes
```

扫描仿真 rows 数组每项需包含：`link_bandwidth_gbps`, `total_latency_s`, `effective_compute_pflops`, `bottleneck_stage`, `decode_latency_s_per_token`, `decode_total_latency_s`, `decode_effective_compute_pflops`, `decode_energy_efficiency_tokens_per_j`, `decode_bottleneck`

## 本轮需完成的工作
完成以上所有步骤，确保项目可独立运行、前端可展示、API 返回 Mock 数据。

## 修复说明写入路径
完成后将 summary 写入：/share/guolidong-nfs/SeeSpace/SCSP-Viz/tasks/extract-viz-v1/impl/round-0-summary.md

summary 必须包含以下章节：
- 本轮实现内容
- AC 推进情况
- 遗留问题
- Goal Tracker 更新请求
- Lesson Delta
