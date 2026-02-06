#!/usr/bin/env python3
"""
分析 HTML 报告并拆分为可翻译的文本块
"""
import re
import json
import sys
from pathlib import Path
from html.parser import HTMLParser


class TextBlockExtractor(HTMLParser):
    """提取 HTML 中的文本块，保留结构信息"""

    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current_block = []
        self.in_script = False
        self.in_style = False
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag == 'script':
            self.in_script = True
        elif tag == 'style':
            self.in_style = True

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        # 跳过 script 和 style 标签内的内容
        if self.in_script or self.in_style:
            return

        # 跳过纯空白
        text = data.strip()
        if not text:
            return

        # 记录文本块及其所在的标签上下文
        self.blocks.append({
            'text': text,
            'context': ' > '.join(self.tag_stack[-3:]) if self.tag_stack else 'root',
            'length': len(text)
        })


def split_into_chunks(blocks, num_chunks=8):
    """将文本块拆分为指定数量的翻译任务

    策略：按文本长度均衡分配，确保每个任务的文本量相近
    """
    if not blocks:
        return []

    # 计算总长度
    total_length = sum(b['length'] for b in blocks)
    target_chunk_size = total_length // num_chunks

    chunks = []
    current_chunk = []
    current_length = 0

    for block in blocks:
        current_chunk.append(block)
        current_length += block['length']

        # 如果当前块已经达到目标大小，并且不是最后一个块，则创建新块
        if current_length >= target_chunk_size and len(chunks) < num_chunks - 1:
            chunks.append(current_chunk)
            current_chunk = []
            current_length = 0

    # 添加最后一个块
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def analyze_html(html_path, output_json, num_chunks=8):
    """分析 HTML 文件并生成拆分方案

    Args:
        html_path: HTML 文件路径
        output_json: 输出 JSON 文件路径
        num_chunks: 拆分为几个块（默认 8）
    """
    html_path = Path(html_path)

    if not html_path.exists():
        print(f"错误: 文件不存在 {html_path}", file=sys.stderr)
        sys.exit(1)

    # 读取 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 提取文本块
    extractor = TextBlockExtractor()
    extractor.feed(html_content)

    blocks = extractor.blocks
    total_blocks = len(blocks)
    total_chars = sum(b['length'] for b in blocks)

    print(f"分析完成:")
    print(f"  - 总文本块数: {total_blocks}")
    print(f"  - 总字符数: {total_chars}")
    print(f"  - 目标拆分数: {num_chunks}")

    # 拆分为多个块
    chunks = split_into_chunks(blocks, num_chunks)

    # 生成输出
    result = {
        'total_blocks': total_blocks,
        'total_chars': total_chars,
        'num_chunks': len(chunks),
        'chunks': []
    }

    for i, chunk in enumerate(chunks, 1):
        chunk_chars = sum(b['length'] for b in chunk)
        result['chunks'].append({
            'id': i,
            'block_count': len(chunk),
            'char_count': chunk_chars,
            'blocks': chunk
        })

    # 保存为 JSON
    output_path = Path(output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n拆分方案已保存到: {output_json}")
    print(f"\n各块统计:")
    for chunk in result['chunks']:
        print(f"  块 {chunk['id']}: {chunk['block_count']} 个文本块, {chunk['char_count']} 字符")

    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python analyze_html.py <html文件> <输出json> [块数量=8]")
        sys.exit(1)

    html_file = sys.argv[1]
    output_file = sys.argv[2]
    num_chunks = int(sys.argv[3]) if len(sys.argv) > 3 else 8

    analyze_html(html_file, output_file, num_chunks)
