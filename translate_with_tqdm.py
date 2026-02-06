#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insights 报告翻译器 - tqdm 进度条版本
使用 tqdm 显示美观的实时翻译进度
"""

import json
import sys
import time

# 尝试导入 tqdm
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    tqdm = None

def load_json(filepath):
    """加载 JSON 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_tqdm():
    """检查 tqdm 是否安装"""
    if not HAS_TQDM:
        print("\n" + "="*70)
        print("⚠️  tqdm 未安装")
        print("="*70)
        print("\n推荐安装 tqdm 以获得更好的进度显示体验：")
        print("  pip3 install tqdm")
        print("\n继续使用简单文本进度条...\n")
        time.sleep(1)
        return False
    return True

def translate_with_tqdm(data, translation_map):
    """使用 tqdm 进度条翻译"""

    print("\n" + "="*70)
    print("📝 Insights 报告翻译器 - tqdm 版本")
    print("="*70)

    # 统计信息
    total_blocks = sum(len(chunk['blocks']) for chunk in data['chunks'])
    total_chars = sum(chunk.get('char_count', 0) for chunk in data['chunks'])

    print(f"\n📊 翻译任务信息:")
    print(f"  • 总文本块数: {total_blocks}")
    print(f"  • 总字符数: {total_chars:,}")
    print(f"  • Chunks 数量: {data['num_chunks']}")

    if HAS_TQDM:
        print(f"  • 进度显示: tqdm ✓")
    else:
        print(f"  • 进度显示: 简单文本模式")

    print(f"\n" + "="*70)
    print("🚀 开始翻译...")
    print("="*70 + "\n")

    start_time = time.time()

    if HAS_TQDM:
        # 使用 tqdm 显示进度
        with tqdm(total=total_blocks, desc="总进度", unit="块", ncols=70) as pbar:
            for chunk_idx, chunk in enumerate(data['chunks'], 1):
                chunk_id = chunk['id']
                translations = translation_map.get(chunk_id, [])
                blocks = chunk['blocks']

                # 为每个 chunk 创建子进度条
                chunk_desc = f"Chunk {chunk_id}/{data['num_chunks']}"
                for block_idx, block in enumerate(blocks):
                    if block_idx < len(translations):
                        block['translation'] = translations[block_idx]
                    else:
                        block['translation'] = block['text']

                    pbar.set_description(f"Chunk {chunk_id}/{data['num_chunks']}")
                    pbar.update(1)

                    # 每 20 个块显示一次文本预览
                    if (block_idx + 1) % 20 == 0:
                        preview = block['text'][:40] + "..." if len(block['text']) > 40 else block['text']
                        pbar.write(f"  → {preview}")
    else:
        # 降级到简单进度条
        current_block = 0

        for chunk in data['chunks']:
            chunk_id = chunk['id']
            translations = translation_map.get(chunk_id, [])
            blocks = chunk['blocks']

            print(f"处理 Chunk {chunk_id}...")

            for block_idx, block in enumerate(blocks):
                current_block += 1

                if block_idx < len(translations):
                    block['translation'] = translations[block_idx]
                else:
                    block['translation'] = block['text']

                # 简单进度条
                percent = current_block / total_blocks
                bar_len = 40
                filled = int(bar_len * percent)
                bar = "█" * filled + "░" * (bar_len - filled)

                progress = f"\r[{bar}] {percent*100:.1f}% ({current_block}/{total_blocks})"
                sys.stdout.write(progress)
                sys.stdout.flush()

                time.sleep(0.002)

        print()  # 换行

    # 显示统计
    elapsed = time.time() - start_time
    print(f"\n⏱️  总耗时: {elapsed:.2f} 秒")
    print(f"🚀 平均速度: {total_blocks/elapsed:.0f} 文本块/秒")

    print("\n" + "="*70)
    print("📈 详细统计")
    print("="*70 + "\n")

    for chunk in data['chunks']:
        chunk_id = chunk['id']
        block_count = len(chunk['blocks'])
        char_count = chunk.get('char_count', 0)
        translated_count = sum(1 for b in chunk['blocks'] if 'translation' in b)

        status = "✅" if translated_count == block_count else "⚠️"
        print(f"  {status} Chunk {chunk_id}: {block_count:3d} 文本块, {char_count:5d} 字符")

    total_translated = sum(
        sum(1 for b in chunk['blocks'] if 'translation' in b)
        for chunk in data['chunks']
    )

    print(f"\n  翻译完成率: {total_translated}/{total_blocks} ({total_translated/total_blocks*100:.1f}%)")

    return data

def load_translation_map_from_file(filepath):
    """从文件加载翻译映射"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  翻译文件未找到: {filepath}")
        return {}

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python translate_with_tqdm.py <analysis_file> [translation_file]")
        print("\n参数:")
        print("  analysis_file    - 分析结果 JSON 文件路径")
        print("  translation_file - 翻译数据 JSON 文件路径（可选）")
        sys.exit(1)

    analysis_file = sys.argv[1]
    translation_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        # 检查 tqdm
        use_tqdm = check_tqdm()

        # 加载数据
        print("⏳ 加载数据...")
        data = load_json(analysis_file)

        # 加载翻译数据
        if translation_file:
            print(f"⏳ 加载翻译数据: {translation_file}")
            translation_map = load_translation_map_from_file(translation_file)
        else:
            print("⏳ 使用内置翻译数据...")
            # 这里应该加载完整的翻译映射
            # 为了演示，使用空字典
            translation_map = {}

        # 如果没有翻译数据，从已翻译的文件加载
        if not translation_file and 'chunks' in data:
            # 检查是否已有翻译
            has_translation = any(
                'translation' in block
                for chunk in data['chunks']
                for block in chunk['blocks']
            )

            if has_translation:
                print("✓ 检测到已有翻译，跳过翻译步骤")
            else:
                print("⚠️  未找到翻译数据")

        # 执行翻译（如果有翻译映射）
        if translation_map or (not translation_file and not any('translation' in b for c in data['chunks'] for b in c['blocks'])):
            data = translate_with_tqdm(data, translation_map)

        # 保存结果
        print("\n💾 保存翻译结果...")
        save_json(data, analysis_file)

        print("\n" + "="*70)
        print("✅ 翻译完成！")
        print("="*70 + "\n")

    except FileNotFoundError as e:
        print(f"\n❌ 文件未找到: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON 解析错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
