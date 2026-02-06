# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Claude Code skill 插件，用于将现有的 insights HTML 报告自动翻译为中文。

- **仓库名称**: insights-zh
- **许可证**: MIT License
- **主要功能**: 检查现有的 insights HTML 报告、翻译为中文、将翻译后的文件复制到当前工作目录

## 项目架构

本项目作为一个 Claude Code skill 实现，核心工作流程分为三个独立的 task：

1. **检查报告文件**
   - 检查 `~/.claude/usage-data/report.html` 是否存在
   - 如果不存在则向用户报告错误

2. **翻译 HTML 报告**
   - 读取 `~/.claude/usage-data/report.html` 文件
   - 使用大模型将内容翻译为中文
   - **关键要求**: 保留原文的样式、布局和格式结构（如 HTML 标签、CSS 样式、JavaScript 代码等）

3. **复制并重命名文件**
   - 将翻译后的报告复制到当前工作目录
   - 命名为 `report-zh.html`
   - 原始 `report.html` 保持不变

## 开发注意事项

- 使用中文与用户交互
- 翻译时必须保留 HTML 的原始格式和结构
- 不执行 insights 命令，只处理已存在的报告文件
