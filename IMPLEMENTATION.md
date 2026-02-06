# Insights-ZH 技能实施文档

## 实施日期
2025-02-06 (重构版本)

## 实施内容

已成功重构 `insights-zh` Claude Code skill，该技能检查现有的 insights HTML 报告并将其翻译为中文。

## 文件结构

```
~/.claude/skills/insights-zh/
├── SKILL.md                  # 主技能文件
├── analyze_html.py           # HTML 分析脚本
├── merge_translations.py     # 翻译合并脚本
└── rules/
    └── translation-guide.md  # HTML 翻译规则和示例
```

## 技能规格

### 基本信息
- **技能名称**: insights-zh
- **调用方式**: `/insights-zh` (仅用户手动调用)
- **报告格式**: HTML
- **输出文件**: `report-zh.html` (当前工作目录)
- **源文件**: `~/.claude/usage-data/report.html` (保持不变)

### 功能描述

该技能通过 **7 个独立的 task** 完成，相比原来的 3 个任务，新架构更加精细和可靠：

1. **Task 1: 检查报告文件**
   - 检查 `~/.claude/usage-data/report.html` 是否存在
   - 如果不存在则向用户报告错误并终止

2. **Task 2: 分析 HTML 文本块**
   - 调用 `analyze_html.py` 脚本分析 HTML 文件
   - 计算文本块数量和总字符数
   - 将文本块拆分为 8-10 个均衡的部分
   - 生成分析结果到 `/tmp/insights-analysis.json`

3. **Task 3: 创建翻译子任务**
   - 读取分析结果 JSON 文件
   - 根据 `chunks` 数组创建翻译子任务列表
   - 准备翻译工作流程

4. **Task 4: 执行翻译**
   - 串行执行所有翻译子任务
   - 对于每个子任务：
     * 读取对应的文本块
     * 使用大模型将英文翻译为中文
     * 保存翻译结果到 JSON 文件
   - 保留所有 HTML 标签、CSS 样式、JavaScript 代码

5. **Task 5: 整合翻译结果**
   - 调用 `merge_translations.py` 脚本
   - 将原始 HTML 和翻译结果合并
   - 生成完整的中文 HTML 文件到 `/tmp/report-zh.html`
   - 保持原有的布局、颜色、风格等所有视觉元素

6. **Task 6: 复制到当前目录**
   - 将翻译后的文件复制到当前工作目录
   - 命名为 `report-zh.html`
   - 原始 `report.html` 保持不变

7. **Task 7: 在浏览器中打开**
   - 使用系统默认浏览器打开翻译后的报告
   - 自动查看最终结果

## 架构优势

### 相比原架构的改进

1. **更好的任务拆分**
   - 原 3 任务 → 新 7 任务
   - 每个任务职责更加单一和清晰
   - 更容易调试和定位问题

2. **更可靠的翻译机制**
   - 自动分析 HTML 结构
   - 智能拆分文本块（按长度均衡）
   - 避免单次翻译内容过长导致的问题

3. **更好的可维护性**
   - 独立的 Python 脚本处理 HTML
   - 清晰的数据流（JSON 中间文件）
   - 每个步骤都可以独立测试

4. **更友好的用户体验**
   - 自动在浏览器中打开结果
   - 更详细的进度反馈
   - 更清晰的错误提示

## 关键特性

### HTML 翻译规则
- ✅ 保留所有 HTML 标签和属性
- ✅ 保留 `<style>` 标签内的 CSS 代码
- ✅ 保留 `<script>` 标签内的 JavaScript 代码
- ✅ 保留代码块中的技术术语
- ✅ 翻译所有用户可见的文本内容
- ✅ 保持 HTML 结构和格式完整

### 文本块分析策略
- 使用 Python HTMLParser 解析 HTML
- 提取所有非 script/style 标签内的文本
- 记录每个文本块的上下文（标签层级）
- 按字符长度均衡分配到 8-10 个块

### 翻译策略
- 串行执行确保上下文一致性
- 每个块独立翻译，避免长度限制
- 保留技术术语的原始形式
- 维护 HTML 结构完整性

### 合并策略
- 按文本长度降序替换，避免短文本被先替换
- 精确匹配原始文本
- 保留所有 HTML 标签和属性
- 只替换文本节点内容

## 任务依赖关系

```
Task 1 (检查文件)
  ↓
Task 2 (分析 HTML)
  ↓
Task 3 (创建子任务)
  ↓
Task 4 (执行翻译)
  ↓
Task 5 (整合结果)
  ↓
Task 6 (复制文件)
  ↓
Task 7 (打开浏览器)
```

## 使用方法

### 基本调用

1. 首先运行 insights 命令生成报告：

```bash
/insights
```

2. 然后运行本技能翻译报告：

```bash
/insights-zh
```

### 预期行为

1. 技能会自动创建 7 个 task
2. 按依赖顺序执行任务
3. 在当前目录生成 `report-zh.html` 文件
4. 自动在浏览器中打开翻译后的报告
5. 原始 `~/.claude/usage-data/report.html` 保持不变

## 测试验证

### 验证步骤

1. **确认技能已安装**
   ```bash
   ls -la ~/.claude/skills/insights-zh/
   ```

2. **测试调用**
   - 在任意项目目录运行 `/insights-zh`
   - 检查是否成功创建 7 个 task

3. **验证输出**
   - 检查当前目录是否生成 `report-zh.html`
   - 在浏览器中打开 HTML 文件
   - 验证：
     - 中文翻译准确
     - HTML 格式完整
     - CSS 样式正常
     - 页面布局正确

### 预期结果

成功执行后应该看到：

```
✅ Insights 中文报告生成完成！

生成的文件：
- report-zh.html (当前目录)

原始报告：~/.claude/usage-data/report.html (未修改)

已在浏览器中打开翻译后的报告。
```

## 技术实现

### 允许使用的工具

```yaml
allowed-tools:
  - TaskCreate    # 创建任务
  - TaskUpdate    # 更新任务状态
  - TaskList      # 列出任务
  - TaskGet       # 获取任务详情
  - Bash          # 执行命令
  - Read          # 读取文件
  - Write         # 写入文件
```

### 文件处理逻辑

1. **检查报告文件**: 验证 `~/.claude/usage-data/report.html` 是否存在
2. **分析 HTML**: 使用 Python 脚本提取和拆分文本块
3. **翻译处理**: 保留 HTML 结构，只翻译文本节点
4. **合并结果**: 将翻译结果合并回 HTML
5. **文件输出**: 复制到当前工作目录

### 中间文件

```
/tmp/insights-analysis.json  # 分析结果和翻译数据
/tmp/report-zh.html          # 合并后的中文 HTML（临时）
./report-zh.html             # 最终输出文件
```

## 脚本说明

### analyze_html.py

**功能**: 分析 HTML 文件并拆分文本块

**用法**:
```bash
python3 analyze_html.py <html文件> <输出json> [块数量=8]
```

**输出**: JSON 文件，包含：
- `total_blocks`: 总文本块数
- `total_chars`: 总字符数
- `num_chunks`: 拆分的块数
- `chunks`: 每个块的详细信息

**特性**:
- 使用 HTMLParser 解析 HTML
- 跳过 script 和 style 标签
- 记录文本块的上下文
- 按长度均衡分配块

### merge_translations.py

**功能**: 将翻译结果合并回 HTML

**用法**:
```bash
python3 merge_translations.py <原始html> <翻译json> <输出html>
```

**输出**: 完整的中文 HTML 文件

**特性**:
- 按文本长度降序替换
- 精确匹配原始文本
- 保留 HTML 结构
- 只替换文本节点

## 故障排除

### 问题 1: 找不到 HTML 文件

**检查方法**:
```bash
ls -la ~/.claude/usage-data/report.html
```

**可能原因**:
- 未运行 `/insights` 命令生成报告
- 报告文件被移动或删除

**解决方法**:
先运行 `/insights` 命令生成报告，然后再运行 `/insights-zh`

### 问题 2: 分析脚本执行失败

**检查方法**:
```bash
python3 --version
ls -la ~/.claude/skills/insights-zh/analyze_html.py
```

**可能原因**:
- Python 3 未安装
- 脚本文件不存在
- 脚本没有执行权限

**解决方法**:
```bash
# 安装 Python 3 (如果需要)
# 确保脚本存在并可执行
chmod +x ~/.claude/skills/insights-zh/analyze_html.py
chmod +x ~/.claude/skills/insights-zh/merge_translations.py
```

### 问题 3: 翻译后 HTML 格式错误

**检查方法**:
- 在浏览器中打开 HTML 文件
- 使用 HTML 验证工具

**可能原因**:
- HTML 标签被误翻译
- CSS 代码被修改
- 属性值被改变

**解决方法**:
检查翻译规则是否正确应用，确保只翻译文本节点

### 问题 4: 浏览器无法打开

**检查方法**:
```bash
ls -la ./report-zh.html
```

**可能原因**:
- 文件未成功复制
- 浏览器命令不正确

**解决方法**:
- 手动在浏览器中打开 `./report-zh.html` 文件
- 检查系统命令（macOS: open, Linux: xdg-open, Windows: start）

## 参考文档

- **主技能文件**: `~/.claude/skills/insights-zh/SKILL.md`
- **分析脚本**: `~/.claude/skills/insights-zh/analyze_html.py`
- **合并脚本**: `~/.claude/skills/insights-zh/merge_translations.py`
- **翻译指南**: `~/.claude/skills/insights-zh/rules/translation-guide.md`
- **Claude Code 技能文档**: https://docs.anthropic.com/claude-code/skills

## 后续改进建议

1. **增加配置选项**: 允许用户自定义输出文件名和块数量
2. **支持多语言**: 扩展为支持其他语言翻译
3. **增量翻译**: 支持只翻译新增或修改的内容
4. **翻译缓存**: 缓存已翻译内容避免重复翻译
5. **质量检查**: 自动验证翻译后的 HTML 格式
6. **批量翻译**: 支持翻译多个历史报告
7. **并行翻译**: 支持并行处理多个翻译子任务（需要解决上下文一致性问题）

## 许可证

MIT License - 与项目保持一致

## 联系方式

如有问题或建议，请在 GitHub 仓库提交 Issue：
https://github.com/agiray/insights-zh
