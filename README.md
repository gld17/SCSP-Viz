# SCSP-Viz 星座智算可视化分析软件 V1.0

SCSP-Viz 是从 SCSP 仿真平台提取出的独立可视化交付层。项目保留配置校验、实验记录、结果导出、前端展示和标准化 REST API，不执行真实仿真计算；所有仿真结果由 `scsp_viz.mock_engine` 生成，便于演示、集成联调和可视化验收。

## 功能特性

- 独立 FastAPI 服务，不依赖 SCSP_v0 源码包。
- 提供单点仿真 Mock API，返回与 v0 `SimulationMetrics` 对齐的完整指标结构。
- 提供带宽扫描 Mock API，返回 knee bandwidth、knee reason 和扫描 rows。
- 支持实验运行、实验记录 JSONL 存储、结果 JSON/CSV 输出。
- 支持实验复现实验接口，基于 Mock 数据生成对比摘要。
- 保留配置标准化与校验层，用于前端表单展示和接口输入检查。
- 保留扫描延迟可视化函数，可从 CSV 或 JSON 实验结果文件绘图。
- 提供静态前端页面、资产和模型注册表配置文件，便于离线展示。

## 目录结构

```text
SCSP-Viz/
├── assets/                         # 前端静态图片资产
├── configs/                        # 前端展示用配置数据
├── experiments/                    # 示例实验记录与运行结果
├── scsp_viz/                       # 独立 Python 包
│   ├── config.py                   # V1 配置模型、标准化和校验
│   ├── experiment.py               # 实验记录、运行、复现和摘要
│   ├── mock_engine.py              # Mock 单点/扫描数据生成器
│   ├── models.py                   # 指标 dataclass
│   ├── visualization.py            # 结果文件绘图
│   └── web_api.py                  # REST API 与静态页面服务
├── tests/                          # Mock API 与实验层测试
├── web/index.html                  # 前端页面
├── requirements.txt                # 运行依赖
└── run_web.py                      # 启动脚本
```

## 安装依赖

```bash
cd /share/guolidong-nfs/SeeSpace/SCSP-Viz
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

运行测试还需要安装 `pytest`：

```bash
pip install pytest
pytest
```

## 启动方式

```bash
python run_web.py
```

默认监听 `0.0.0.0:8000`，浏览器访问 `http://localhost:8000/` 查看前端页面。

## 接口说明

SCSP-Viz 按 SCSP 仿真平台的标准化 REST API 交互规范暴露可视化层接口，输入字段保持 `config` 字典形式，输出结构保持单点、扫描和实验记录的标准形态。当前版本所有计算结果均来自 Mock 数据层。

- `GET /api/health`：健康检查，返回 `{"status": "ok"}`。
- `POST /api/simulations/single`：单点仿真 Mock。请求体包含 `config` 和可选 `bandwidth_gbps`，返回 `mode=config=metrics`。
- `POST /api/simulations/sweep`：带宽扫描 Mock。请求体包含 `config` 和可选 `bandwidths_gbps`，返回 `mode=knee_bandwidth_gbps=knee_reason=rows`。
- `POST /api/experiments/run`：运行 Mock 实验，输出实验记录、结果 JSON，扫描模式额外输出 CSV。
- `GET /api/experiments`：读取 JSONL 实验记录列表。
- `GET /api/experiments/{experiment_id}`：读取单条实验记录。
- `POST /api/experiments/reproduce/{experiment_id}`：基于历史输入配置重新生成 Mock 结果并返回摘要差异。
- `GET /api/experiments/{experiment_id}/export`：导出实验记录 JSON。

## 前端页面说明

`web/index.html` 是 SCSP-Viz 的单页可视化界面，通过同源 API 调用 `/api/simulations/*` 与 `/api/experiments/*`。页面会读取 `/assets/earth-horizon-reference.png` 和 `/configs/model_registry.json` 用于展示与表单选项，但后端不会依赖模型注册表执行真实计算。

## 许可证声明

本项目作为 SCSP-Viz 星座智算可视化分析软件 V1.0 交付层示例，许可证和对外发布范围以项目所有者后续声明为准。未获得授权前，不得将项目代码、资产或接口文档用于未许可的商业分发。
