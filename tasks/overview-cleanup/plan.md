# 概览页面清理与 README 英文化

## Goal Description
对 SCSP-Viz 前端概览页面进行精简：删除下半部分的"性能分析"大卡片，使"实验配置概览"卡片独占下半部分；同时将 README.md 从中文翻译为英文版本。

## Acceptance Criteria

- AC-1: 概览页面删除性能分析卡片
  - Positive Tests：
    - 打开概览页面，下半部分（overview-row2）只显示"实验配置概览"一个卡片
    - 页面上不存在"性能分析"标题和相关的 tab 切换控件
    - 页面上不存在时延分解甜甜圈图、带宽敏感性折线图、算力敏感性折线图
  - Negative Tests：
    - 概览页面上半部分（星座构型、任务流程、关键指标）保持原样不变
    - 其他页面（实验管理、星座配置、模型配置等）不受影响

- AC-2: 清理性能分析相关的废弃 CSS 和 JS
  - Positive Tests：
    - 删除 `.perf-panel`、`.donut`、`.donut-wrap`、`.donut-center` 等仅在性能分析中使用的 CSS 规则
    - 删除 JS 中 `perf-panel-*` 相关的 tab 切换逻辑和 `drawDonut` / `drawLineChart` 中对性能分析图表的调用
    - 删除 `bwSensitivityChart` 和 `computeSensitivityChart` canvas 元素
  - Negative Tests：
    - 不删除实验配置概览的渲染逻辑（`renderConfigSummary` 等）
    - 不删除星座构型场景的渲染逻辑

- AC-3: README.md 改为英文版本
  - Positive Tests：
    - README.md 全文为英文
    - 保留原有的 Markdown 格式和结构（标题层级、代码块、目录树等）
    - 翻译准确，技术术语保持专业
  - Negative Tests：
    - 不出现中文内容（专有名词如 SCSP、SCSP-Viz 等保留原文）
    - 不改变文档中的目录结构、文件路径、接口路径

- AC-4: 无回归
  - Positive Tests：
    - 页面正常加载，无控制台报错
    - 概览页面上半部分功能（KPI 指标展示、星座场景图、任务流程）正常
    - 实验配置概览卡片正常渲染
  - Negative Tests：
    - 不引入新的语法错误或 HTML 结构错误
    - 不破坏其他页面的导航和显示

## Implementation Notes
- 代码中禁止出现 AC-、Milestone、Step、Phase 等 plan 标记
- 修改前先在文件中搜索所有引用，确认删除的安全性
- HTML/CSS/JS 的修改保持最小化，只删除明确属于"性能分析"的部分
- README 翻译保持技术文档风格，代码块和路径不变

## Path Boundaries
- 可接受的实现范围：web/index.html 的概览页面区域、README.md 的全文翻译
- 不可接受的方向：修改后端 API、修改其他页面的功能、添加新的功能
- 不得修改的文件：scsp_viz/*.py、tests/、configs/、assets/、run_web.py、requirements.txt
