NO_ISSUES

## REVIEW LOOP - Round 0 Diff Review

### 变更范围
- `web/index.html`: 删除性能分析卡片及相关 CSS/JS（-172 行）
- `README.md`: 中文翻译为英文（-88 行 +88 行，实质改写）
- 新增 PBR 任务产物（plan.md、state.json、gate.sh、impl/ 文件）

### 逐项检查

#### P0（功能错误/安全风险）：无
- 概览页面上半部分（星座构型、任务流程、关键指标）保持完整
- 实验配置概览卡片保留且正常渲染
- 其他页面导航和结构未受影响

#### P1（逻辑缺陷/测试缺失）：无
- `renderDonut()` 和相关性能分析函数已完整删除
- `bindPerformanceTabs()` 及其调用点已完整删除
- `bwSensitivityChart` / `computeSensitivityChart` canvas 及绘制调用已删除
- `.overview-row2` 已正确改为单列布局

#### P2-P9（代码风格/可读性/优化）：无
- `.tabs` / `.tab` 全局 CSS 删除安全：搜索确认其他页面无使用
- `.chart` 基础 CSS 保留，实验结果页 `.chart--perf` 有 `.exp-chart-cell .chart` 覆盖，不受影响
- 注释"圆环"改为"KPI"与改动一致
- README 翻译准确，专有名词保留

### 结论
Diff 干净、精确、无遗漏、无过度删除。输出 NO_ISSUES。
