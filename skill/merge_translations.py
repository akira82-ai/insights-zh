#!/usr/bin/env python3
"""
将翻译后的文本块合并回 HTML 文件
"""
import re
import json
import sys
from pathlib import Path


def merge_translations_to_html(html_path, translations_json, output_html):
    """将翻译结果合并回 HTML

    Args:
        html_path: 原始 HTML 文件路径
        translations_json: 翻译结果 JSON 文件路径
        output_html: 输出 HTML 文件路径
    """
    html_path = Path(html_path)

    # 读取原始 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 读取翻译结果
    with open(translations_json, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    # 按顺序合并所有翻译
    # 这里我们使用简单的文本替换策略
    # 为了更准确，我们应该按照原始文本块的顺序进行替换

    # 收集所有需要替换的文本
    replacements = []
    for chunk in translations['chunks']:
        for block in chunk['blocks']:
            original_text = block['text']
            translated_text = block.get('translation', original_text)
            replacements.append((original_text, translated_text))

    # 按文本长度降序排序，避免短文本被先替换导致长文本匹配失败
    replacements.sort(key=lambda x: len(x[0]), reverse=True)

    # 执行替换
    merged_html = html_content
    replace_count = 0

    for original, translated in replacements:
        if original != translated:
            # 使用精确匹配替换，只替换第一个匹配
            merged_html = merged_html.replace(original, translated, 1)
            replace_count += 1

    # 保存合并后的 HTML
    output_path = Path(output_html)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(merged_html)

    print(f"合并完成:")
    print(f"  - 替换了 {replace_count} 个文本块")
    print(f"  - 输出文件: {output_html}")

    return merged_html


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法: python merge_translations.py <原始html> <翻译json> <输出html>")
        sys.exit(1)

    html_file = sys.argv[1]
    translations_file = sys.argv[2]
    output_file = sys.argv[3]

    merge_translations_to_html(html_file, translations_file, output_file)
