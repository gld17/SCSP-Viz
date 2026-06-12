# Round 0 任务

## 强制执行规则
你必须遵守 pbr-codex-builder skill。若未加载该 skill，也必须遵守：
1. 你是唯一 Builder，只写代码。
2. 不做 review 判断。
3. 不执行任何 git 命令。
4. 完成后必须写入指定 summary 文件。

## 重要限制
- **不要执行 git 命令**：如果你需要重命名文件，请直接创建新文件并写入内容，然后删除旧文件。不要尝试 `git mv`（你会被拒绝）。Kimi 会在后续 commit 阶段处理 git 历史追溯性。
- 所有文件操作（创建、修改、删除）通过 Hermes 工具完成，不直接输出代码到对话中。
- 每次修改文件后，检查是否有 include 路径、import 路径或其他引用需要同步更新。
- 修改前先在相关文件中搜索所有引用，确认修改的安全性。

## 本轮需完成的工作

### 工作 1：删除概览页面的"性能分析"大卡片

在 `/share/guolidong-nfs/SeeSpace/SCSP-Viz/web/index.html` 中：

1. **删除 HTML**：找到 `<section class="overview-row2">`，删除其中第二个 `.card`（标题为"性能分析"的卡片），只保留第一个"实验配置概览"卡片。同时将 `.overview-row2` 的 grid 布局改为单列（因为只剩一个卡片）。

2. **删除 CSS**：找到并删除以下仅在性能分析中使用的 CSS 规则：
   - `.perf-panel` 和 `.perf-panel.active`
   - `.donut-wrap`
   - `.donut` 及其子规则（`.donut svg`, `.donut-center`, `.donut .donut-center`）
   - `.donut-center .big` 和 `.donut-center .sub`
   - `.legend-item`
   - `.overview-row2 > .card > .tabs` 相关规则
   - `.overview-row2 > .card > .perf-panel` 相关规则
   - `.overview-row2 > .card > .perf-panel .donut-wrap`
   - `.overview-row2 > .card > .perf-panel .chart.chart--perf`
   - `.main.main--overview #page-overview .donut-center .big`
   - `.main.main--overview #page-overview .donut-center .sub`
   - `.main.main--overview #page-overview .overview-row2 > .card > .perf-panel .donut-wrap`
   - `.main.main--overview #page-overview .overview-row2 .donut`
   - `.chart`（但只删除 `.chart--perf` 相关部分，其他页面的 `.chart` 保留）
   - 注意：`.tabs` 和 `.tab` 可能在其他页面也使用，不要全局删除，只删除概览页面专用的样式

3. **删除 JS**：
   - 删除 `bwSensitivityChart` 和 `computeSensitivityChart` 两个 canvas 元素的创建/引用
   - 删除 `perf-panel-decompose`、`perf-panel-bandwidth`、`perf-panel-compute` 相关的 tab 切换逻辑
   - 删除 `drawDonut` 函数中对性能分析 donut 的绘制（如果 `drawDonut` 只用于性能分析则整个删除，如果还有其他用途则保留）
   - 删除 `drawLineChart` 调用中针对 `bwSensitivityChart` 和 `computeSensitivityChart` 的调用
   - 保留 `renderConfigSummary` 等实验配置概览的渲染逻辑
   - 保留星座构型场景的渲染逻辑

### 工作 2：将 README.md 翻译为英文

将 `/share/guolidong-nfs/SeeSpace/SCSP-Viz/README.md` 的内容从中文翻译为英文。要求：
- 保留原有的 Markdown 格式和结构（标题层级、代码块、目录树等）
- 翻译准确，技术术语保持专业
- 专有名词如 SCSP、SCSP-Viz 等保留原文
- 代码块和文件路径不变

### 验证
修改完成后，检查：
- 页面正常加载无报错
- overview-row2 只剩一个"实验配置概览"卡片
- 页面上没有"性能分析"标题和 tab 控件
- README.md 全文为英文

## 完成后
将 summary 写入：/share/guolidong-nfs/SeeSpace/SCSP-Viz/tasks/overview-cleanup/impl/round-0-summary.md
