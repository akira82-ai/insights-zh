# insights-zh

> Claude Code 技能插件 - 自动翻译 Insights 报告为中文

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-blue.svg)](https://docs.anthropic.com/claude-code/skills)

## 简介

`insights-zh` 是一个 Claude Code skill 插件，用于将 Claude Code 的 insights 命令生成的 HTML 报告自动翻译为中文。

### 特性

- ✅ **自动分析**: 智能拆分 HTML 文本块，确保翻译质量和效率
- ✅ **保持格式**: 完整保留原始 HTML 的布局、颜色、样式和结构
- ✅ **精准翻译**: 只翻译用户可见的文本内容，保留代码和技术术语
- ✅ **自动化**: 一键完成从分析到翻译再到浏览器预览的全流程
- ✅ **模块化**: 7 个独立任务，清晰的职责划分，易于调试和维护

## 工作流程

本技能通过 **7 个独立任务** 完成翻译：

```
1. 检查报告文件
   ↓
2. 分析 HTML 文本块（拆分为 8-10 个部分）
   ↓
3. 创建翻译子任务
   ↓
4. 串行执行翻译
   ↓
5. 整合翻译结果为完整 HTML
   ↓
6. 复制到当前工作目录
   ↓
7. 在浏览器中打开查看
```

## 安装

### 前置要求

- Claude Code CLI
- Python 3.x
- 已生成的 insights 报告（通过 `/insights` 命令）

### 安装步骤

1. 克隆本仓库到你的 skills 目录：

```bash
git clone https://github.com/agiray/insights-zh.git ~/.claude/skills/insights-zh
```

2. 确保脚本有执行权限：

```bash
chmod +x ~/.claude/skills/insights-zh/*.py
```

3. 验证安装：

```bash
ls -la ~/.claude/skills/insights-zh/
```

你应该看到：
- `SKILL.md` - 主技能文件
- `analyze_html.py` - HTML 分析脚本
- `merge_translations.py` - 翻译合并脚本
- `rules/translation-guide.md` - 翻译规则

## 使用方法

### 基本用法

1. **生成 insights 报告**：

```bash
/insights
```

2. **翻译报告为中文**：

```bash
/insights-zh
```

3. **查看结果**：

翻译完成后，会在当前目录生成 `report-zh.html` 文件，并自动在浏览器中打开。

### 预期输出

```
✅ Insights 中文报告生成完成！

生成的文件：
- report-zh.html (当前目录)

原始报告：~/.claude/usage-data/report.html (未修改)

已在浏览器中打开翻译后的报告。
```

## 技术架构

### 文件结构

```
~/.claude/skills/insights-zh/
├── SKILL.md                  # 主技能文件（7 个任务定义）
├── analyze_html.py           # HTML 分析和文本块拆分脚本
├── merge_translations.py     # 翻译结果合并脚本
└── rules/
    └── translation-guide.md  # 翻译规则和示例
```

### 核心组件

#### 1. HTML 分析脚本 (analyze_html.py)

**功能**:
- 解析 HTML 结构
- 提取所有文本块
- 智能拆分为 8-10 个均衡的部分
- 生成 JSON 格式的分析结果

**输出格式**:
```json
{
  "total_blocks": 258,
  "total_chars": 16162,
  "num_chunks": 8,
  "chunks": [
    {
      "id": 1,
      "block_count": 38,
      "char_count": 2245,
      "blocks": [
        {
          "text": "Claude Code Insights",
          "context": "head > meta > title",
          "length": 20
        }
      ]
    }
  ]
}
```

#### 2. 翻译合并脚本 (merge_translations.py)

**功能**:
- 读取原始 HTML 文件
- 读取翻译结果 JSON
- 精确替换文本节点
- 保持 HTML 结构完整

**特点**:
- 按长度降序替换，避免短文本误匹配
- 保留所有标签、属性、样式、脚本
- 只替换用户可见的文本内容

#### 3. 技能定义 (SKILL.md)

定义了 7 个独立任务及其依赖关系：

1. **检查报告文件** - 验证源文件存在
2. **分析 HTML 文本块** - 调用分析脚本
3. **创建翻译子任务** - 准备翻译工作流
4. **执行翻译** - 串行翻译所有文本块
5. **整合翻译结果** - 调用合并脚本
6. **复制到当前目录** - 输出最终文件
7. **在浏览器中打开** - 预览结果

## 翻译规则

### 保留不翻译

- HTML 标签和属性名（`class`, `id`, `href`, `style` 等）
- HTML 属性值（`class="container"`, `id="header"` 等）
- CSS 类名和 ID
- `<style>` 标签内的所有 CSS 代码
- `<script>` 标签内的所有 JavaScript 代码
- 代码块中的技术术语和代码片段

### 翻译内容

- 所有用户可见的文本内容
- 页面标题、标题、段落文本
- 按钮文本、链接文本（href 保留）
- 表格内容、列表项文本
- 提示信息和说明文字

### 翻译原则

- 保持 HTML 结构完全不变
- 保持所有标签和属性完整
- 保持缩进和格式
- 只翻译文本节点内容
- 确保翻译后的 HTML 语法正确
- 技术术语保持一致性

## 示例

### 翻译前

```html
<h1>Claude Code Insights</h1>
<p class="subtitle">1,001 messages across 151 sessions</p>
<div class="stat">
  <div class="stat-value">1,001</div>
  <div class="stat-label">Total Messages</div>
</div>
```

### 翻译后

```html
<h1>Claude Code 洞察</h1>
<p class="subtitle">151 个会话中的 1,001 条消息</p>
<div class="stat">
  <div class="stat-value">1,001</div>
  <div class="stat-label">总消息数</div>
</div>
```

## 故障排除

### 问题：找不到 report.html 文件

**错误信息**:
```
❌ 未找到 report.html 文件。请先运行 /insights 命令生成报告。
```

**解决方法**:
1. 先运行 `/insights` 命令生成报告
2. 确认文件存在：`ls -la ~/.claude/usage-data/report.html`

### 问题：分析脚本执行失败

**检查步骤**:
```bash
# 检查 Python 版本
python3 --version

# 检查脚本权限
ls -la ~/.claude/skills/insights-zh/*.py

# 添加执行权限
chmod +x ~/.claude/skills/insights-zh/*.py
```

### 问题：翻译后 HTML 格式错误

**可能原因**:
- HTML 标签被误翻译
- CSS 或 JavaScript 代码被修改

**解决方法**:
检查翻译规则是否正确应用，确保只翻译文本节点内容

### 问题：浏览器无法打开

**解决方法**:
手动在浏览器中打开 `./report-zh.html` 文件

## 开发

### 本地测试

1. 测试分析脚本：

```bash
python3 analyze_html.py ~/.claude/usage-data/report.html /tmp/analysis.json 8
```

2. 查看分析结果：

```bash
cat /tmp/analysis.json | jq .
```

3. 测试合并脚本（需要先手动翻译 JSON 中的文本）：

```bash
python3 merge_translations.py ~/.claude/usage-data/report.html /tmp/analysis.json /tmp/report-zh.html
```

### 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 路线图

### 已完成 ✅

- [x] 基础翻译功能
- [x] HTML 结构保留
- [x] 自动分析拆分文本块
- [x] 7 任务架构重构
- [x] 自动浏览器预览

### 计划中 📋

- [ ] 支持自定义输出文件名
- [ ] 支持其他语言翻译
- [ ] 增量翻译（只翻译新增内容）
- [ ] 翻译缓存机制
- [ ] 批量翻译多个历史报告
- [ ] 翻译质量自动验证
- [ ] 并行翻译优化

## 常见问题

### Q: 为什么需要拆分文本块？

A: Insights 报告通常包含大量文本（16000+ 字符），一次性翻译可能：
- 超出模型的上下文限制
- 导致翻译质量下降
- 难以定位和修复错误

拆分为 8-10 个块可以确保：
- 每个块的翻译质量
- 更好的上下文理解
- 更容易调试和重试

### Q: 为什么要串行翻译而不是并行？

A: 串行翻译可以确保：
1. **术语一致性**: 技术术语在整个文档中保持统一
2. **上下文连贯**: 理解前后文的逻辑关系
3. **风格统一**: 翻译风格保持一致

并行翻译可能导致不同块使用不同的术语翻译，影响整体质量。

### Q: 原始报告会被修改吗？

A: 不会。原始 `~/.claude/usage-data/report.html` 保持完全不变。翻译结果生成新文件 `report-zh.html` 在当前工作目录。

### Q: 支持自定义块数量吗？

A: 当前版本默认拆分为 8 个块。你可以修改 SKILL.md 中的参数，或直接调用脚本时指定块数量：

```bash
python3 analyze_html.py input.html output.json 10  # 拆分为 10 个块
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- GitHub: [agiray/insights-zh](https://github.com/agiray/insights-zh)
- Issues: [提交问题](https://github.com/agiray/insights-zh/issues)

## 致谢

- [Claude Code](https://docs.anthropic.com/claude-code) - 强大的 AI 辅助编程工具
- [Anthropic](https://www.anthropic.com/) - Claude 的开发者

---

**享受你的中文 insights 报告！** 🎉
