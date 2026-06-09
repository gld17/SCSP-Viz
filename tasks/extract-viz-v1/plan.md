# SCSP-Viz V1.0 — 星座智算可视化分析软件

## Goal Description

从 SCSP_v0 仿真平台中拆分并提取可视化交付层，构建独立项目 `SCSP-Viz`（星座智算可视化分析软件 V1.0）。该项目不执行实际仿真计算、不接入仿真引擎后端，但保留标准化 API 接口；核心定位是**实验管理、结果分析与可视化前端网页展示**的工具软件。通过 Mock 数据层和 Stub 接口保证前端所有页面、图表、交互流程可正常展示，为申请软件著作权提供独立、完整、可运行的可视化软件模块。

## Acceptance Criteria

- AC-1: 项目目录结构完整且符合独立软件工程规范
  - Positive Tests：`SCSP-Viz/` 根目录下包含 `README.md`、`requirements.txt`、`scsp_viz/` 应用目录、`web/` 前端静态资源目录、`experiments/` 实验数据目录、`tests/` 测试目录
  - Negative Tests：不出现与真实仿真引擎耦合的代码（如直接 import engine/simulator/pipeline 并调用计算逻辑）

- AC-2: 前端网页完整可展示
  - Positive Tests：启动 Web 服务后访问 `http://localhost:8000/` 可加载深色主题可视化界面，包含：概览仪表盘、星座构型配置页、模型部署配置页、算力节点配置页、通信链路配置页、实验运行页（含单点/扫描/批量模板）、结果分析页（延时-带宽曲线、有效算力、瓶颈占比）、实验管理页（列表/查询/复现/导出）；所有导航切换无 404，所有图表区域正确渲染（使用 Mock 数据填充）
  - Negative Tests：页面不出现空白区域、JS 报错导致交互卡死、CSS 严重错位

- AC-3: 后端 API 结构保留且返回 Mock 数据
  - Positive Tests：FastAPI 提供以下端点且返回结构合规的 JSON：
    - `GET /api/health` → `{"status": "ok"}`
    - `POST /api/simulations/single` → 返回 Mock 单点仿真结果（含 metrics 字段）
    - `POST /api/simulations/sweep` → 返回 Mock 扫描结果（含 rows 数组）
    - `POST /api/experiments/run` → 返回 Mock 实验记录（含 experiment_id、payload）
    - `GET /api/experiments` → 返回实验列表
    - `GET /api/experiments/{id}` → 返回单条实验详情
    - `POST /api/experiments/reproduce/{id}` → 返回 Mock 复现结果
    - `GET /api/experiments/{id}/export` → 返回导出 JSON
  - Negative Tests：API 不报错 500，返回的 JSON 字段与 v0 前端期望的结构一致（字段缺失需补充）

- AC-4: 实验管理与结果分析功能可独立运行
  - Positive Tests：`JsonlExperimentStore` 可正常读写 `experiments/records.jsonl`；支持实验模板（single_point / bandwidth_sensitivity）；支持实验对比；支持 CSV/JSON 导出；结果分析模块可生成延时-带宽曲线图（基于已保存的真实或 Mock 实验数据）
  - Negative Tests：实验管理不依赖外部仿真进程存在即可工作

- AC-5: 配套 README.md 完整
  - Positive Tests：`README.md` 包含：项目简介、功能特性（≥6 项）、目录结构说明、安装依赖步骤、启动方式（`python run_web.py`）、接口说明、前端页面说明、许可证声明；语言为中文
  - Negative Tests：README 不含未实现功能的虚假承诺

- AC-6: 无回归
  - Positive Tests：SCSP_v0 原仓库任何文件均不被修改
  - Negative Tests：不向 SCSP_v0 写入任何内容

## Implementation Notes
- 代码中禁止出现 AC-、Milestone、Step、Phase 等 plan 标记
- 前端 `web/index.html` 从 v0 复制后，需将其中的 `fetch` 目标后端地址保持相对路径（`/api/...`）不变
- Mock 数据应覆盖单点仿真、扫描仿真、实验记录三种场景，数据结构需与 v0 的 `ExperimentRecord` 和仿真结果 JSON schema 对齐
- `config.py` 中的 `V1SimulationConfig` 和 `normalize_raw_config` / `validate_raw_config` / `dump_config_dict` 需保留，作为前端配置校验和展示的 schema 依据（去掉与仿真计算强耦合的默认值推导即可）
- `visualization.py` 保留绘图能力，输入改为从实验结果文件读取而非直接调用引擎
- 所有真实仿真调用（`engine.run_simulation`、`engine.run_sweep`、`experiment.run_experiment` 中的实际 `run_simulation`）均需替换为 Mock 生成器，但保留原函数签名和接口文档
- SCSP-Viz 与 SCSP 仿真平台完全独立，不设共享源码目录，两者间仅通过标准化 REST API 接口交互（接口规范在 README 中说明）
- 为软著充实度，额外构思并预留以下功能模块（至少实现前端页面占位 + API Stub）：
  1. **场景模板库**：预置多种星座构型模板（低轨密集、中轨稀疏、混合编队）
  2. **批量实验对比**：支持多实验并行对比与差异高亮
  3. **报告生成**：一键导出 HTML/PDF 分析报告（前端占位）
  4. **历史趋势分析**：基于实验记录的时间序列趋势图（前端占位 + Mock 数据）
  5. **数据导入**：支持导入外部仿真结果 JSON/CSV 进行可视化展示

## Path Boundaries
- 可接受的实现范围：从 v0 复制并改造 `web/`、`scsp/web_api.py`、`scsp/experiment.py`、`scsp/visualization.py`、`scsp/config.py`、`scsp/io_utils.py`、`run_web.py`；创建 Mock 数据模块；编写 README.md
- 不可接受的方向：修改 SCSP_v0 任何文件；在 SCSP-Viz 中重新实现仿真引擎（engine/simulator/pipeline/model/communication/deployment/metrics）；引入数据库依赖（保持 JSONL 轻量存储）
- 不得修改的文件：SCSP_v0 仓库下所有文件
