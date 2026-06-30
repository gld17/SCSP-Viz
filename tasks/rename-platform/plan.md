# 统一软件名称为 SCSP-Viz

## Goal Description
将软件中出现的"天基计算仿真平台"及其对应的英文表述"SCSP simulation platform"统一替换为"SCSP-Viz"，确保软件简称成为唯一使用的名称。仅修改名称引用，不改动其他任何功能、结构或内容。

## Acceptance Criteria

- AC-1: 前端页面删除"天基计算仿真平台"中文名称
  - Positive Tests：
    - web/index.html 中不再包含"天基计算仿真平台"字符串
    - 页面标题/副标题区域仅显示 SCSP-Viz 相关名称
  - Negative Tests：
    - 不修改页面其他文字内容（如"天基应用配置"等模块名称保留不变）
    - 不改变页面布局、样式或交互逻辑

- AC-2: README.md 中第 62 行的"SCSP simulation platform"替换为"SCSP-Viz"
  - Positive Tests：
    - README.md 第 62 行不再包含"SCSP simulation platform"字符串
    - 替换后句子语法正确、语义连贯
  - Negative Tests：
    - README.md 第 3 行的"extracted from the SCSP simulation platform"保持原样，不做修改
    - 不修改 README.md 的其他任何内容（标题、目录结构、代码块、文件路径、API 路径等）
    - 不引入拼写错误或格式破坏

- AC-3: 无回归
  - Positive Tests：
    - web/index.html 能正常加载，无 HTML 语法错误
    - README.md 保持有效的 Markdown 格式
  - Negative Tests：
    - 不修改任何其他文件
    - 不改变任何功能代码或配置

## Implementation Notes
- 修改前先用 grep 确认所有待替换字符串的位置和上下文
- 替换时保持原有格式（HTML 标签、Markdown 语法）不变
- 仅做字面替换，不重构句子或调整段落结构

## Path Boundaries
- 可接受的实现范围：web/index.html、README.md 中的名称引用替换
- 不可接受的方向：修改后端代码、修改其他页面功能、添加新功能、重构文档结构
- 不得修改的文件：scsp_viz/*.py、tests/、configs/、assets/、run_web.py、requirements.txt、web/index.html 中除名称外的其他内容
