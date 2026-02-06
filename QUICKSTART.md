# insights-zh 快速入门指南

## 5 分钟上手

### 1. 确认前置条件

```bash
# 检查 Claude Code
claude --version

# 检查 Python
python3 --version
```

### 2. 生成 Insights 报告

```bash
/insights
```

等待报告生成完成。

### 3. 翻译为中文

```bash
/insights-zh
```

### 4. 查看结果

翻译完成后，会自动在浏览器中打开 `report-zh.html` 文件。

## 工作流程

```
生成报告 → 翻译中文 → 自动打开浏览器
```

## 输出文件

- **当前目录**: `report-zh.html`
- **原始报告**: `~/.claude/usage-data/report.html` (保持不变)

## 需要帮助？

- 查看 [README.md](README.md) 了解详细功能
- 查看 [IMPLEMENTATION.md](IMPLEMENTATION.md) 了解技术细节
- 提交 [Issue](https://github.com/agiray/insights-zh/issues) 获取支持
