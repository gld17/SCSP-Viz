# Plan Quiz — extract-viz-v1

## Q1
SCSP-Viz 与 SCSP 仿真平台之间的关系是什么？

A. SCSP-Viz 是 SCSP 的内嵌子模块，直接调用 engine 和 simulator 的源码进行仿真计算  
B. SCSP-Viz 与 SCSP 完全独立，不设共享源码目录，两者间仅通过标准化 REST API 接口交互  
C. SCSP-Viz 复用 SCSP_v0 的 web/ 目录作为软链接，前端文件由两个项目共同维护  
D. SCSP-Viz 需要修改 SCSP_v0 的 experiment.py 来实现数据同步

## Q2
在实现范围上，以下哪项属于「不可接受的方向」？

A. 从 v0 复制并改造 web/index.html 作为前端页面  
B. 在 SCSP-Viz 中创建 Mock 数据模块来替代真实仿真引擎调用  
C. 在 SCSP-Viz 中重新实现仿真引擎（engine / simulator / pipeline / model / communication / deployment / metrics）  
D. 编写 README.md 说明项目功能、目录结构和接口规范

## 参考答案（请在回答后核对）
- Q1 正确答案：B
- Q2 正确答案：C
