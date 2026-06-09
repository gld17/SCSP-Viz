[P2]

# REVIEW LOOP - Round 0 Diff Review

## Diff Overview
- 所有源代码文件均为新增（untracked），无对已有 tracked 文件的破坏性修改
- 唯一 modified 文件是 pbr-state.json（PBR 状态更新，非代码变更）

## 关键新增文件审查

### scsp_viz/web_api.py
- ✅ FastAPI app 创建正确
- ✅ 使用 mock_run_simulation / mock_run_sweep，无真实引擎引用
- ✅ StaticFiles 挂载了 web/、assets/、configs/
- ✅ 所有 API 端点保留：health、single、sweep、experiments/*

### scsp_viz/mock_engine.py
- ✅ 完全独立的 Mock 数据生成器
- ✅ 不引用 engine、simulator、model、deployment、communication、pipeline
- ✅ _mock_metrics 返回包含所有 SimulationMetrics 字段的字典
- ✅ mock_run_sweep 返回 knee_bandwidth_gbps、knee_reason、rows（含 9 个必填字段）

### scsp_viz/experiment.py
- ✅ 从 .mock_engine 导入，无真实引擎耦合
- ✅ JsonlExperimentStore、ExperimentRecord、run_experiment、reproduce_experiment 保留
- ✅ run_experiment 内部调用 mock_run_simulation / mock_run_sweep

### scsp_viz/config.py
- ✅ V1SimulationConfig dataclass 保留
- ✅ normalize_raw_config、validate_raw_config、build_simulation_config 保留
- ✅ 无 model_registry 运行时依赖

### tests/test_web_api.py
- ✅ 使用 ASGI 直接调用测试，无需 TestClient
- ✅ 验证 health、single、sweep API 返回结构

### README.md
- ✅ 中文，结构完整

### web/index.html
- ✅ 前端页面完整复制（3627 行）
- ⚠️ [P2] `<title>SCSP 仿真平台</title>` 未更新为 SCSP-Viz 品牌名（非阻塞）

## 结论
所有新增文件符合 plan.md 要求，无真实引擎耦合，无破坏性修改。唯一的 P2 问题（前端 title）不影响功能展示。
