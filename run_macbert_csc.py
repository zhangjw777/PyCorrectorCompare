# -*- coding: utf-8 -*-
"""
MacBERT-CSC 模型评估脚本

专门用于运行 MacBERT-CSC 模型的评估
支持从文件或直接从列表加载数据
"""

import argparse
import json
import os
from typing import List

from data.data_loader import DataLoader
from main import run_evaluation


# ===================================
# 预留数据集位置 - 在此处填入错误句子列表
# ===================================
ERROR_SENTENCES = [
    # TODO: 在这里添加错误句子列表
    # 每个句子都应该是包含错误的句子
    # 示例：
    # "今天天汽很好",
    # "我门一起去公园",
]


def load_data_from_file(file_path: str) -> List[str]:
    """
    从文件加载数据
    
    Args:
        file_path: 数据文件路径
        
    Returns:
        句子列表
    """
    loader = DataLoader()
    return loader.load_from_file(file_path)


def run_from_list(sentences: List[str], save: bool = True, verbose: bool = True):
    """
    使用列表中的句子运行评估
    
    Args:
        sentences: 错误句子列表
        save: 是否保存结果
        verbose: 是否打印详细信息
    """
    if not sentences:
        print("错误: 句子列表为空!")
        print("请在 ERROR_SENTENCES 中填入错误句子列表，或使用 --file 参数指定数据文件")
        return None
    
    return run_evaluation(
        sentences=sentences,
        model_name="macbert_csc",
        save_results=save,
        verbose=verbose
    )


def run_from_file(file_path: str, save: bool = True, verbose: bool = True):
    """
    从文件加载句子并运行评估
    
    Args:
        file_path: 数据文件路径
        save: 是否保存结果
        verbose: 是否打印详细信息
    """
    sentences = load_data_from_file(file_path)
    print(f"从文件加载了 {len(sentences)} 个句子")
    
    return run_evaluation(
        sentences=sentences,
        model_name="macbert_csc",
        save_results=save,
        verbose=verbose
    )


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MacBERT-CSC 模型检错评估")
    parser.add_argument(
        "--file", "-f",
        type=str,
        default=None,
        help="输入数据文件路径（支持 .txt 或 .json 格式）"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存结果到文件"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，不打印详细信息"
    )
    
    args = parser.parse_args()
    
    save_results = not args.no_save
    verbose = not args.quiet
    
    if args.file:
        # 从文件加载数据
        results = run_from_file(
            file_path=args.file,
            save=save_results,
            verbose=verbose
        )
    else:
        # 使用预定义的句子列表
        results = run_from_list(
            sentences=ERROR_SENTENCES,
            save=save_results,
            verbose=verbose
        )
    
    return results


if __name__ == "__main__":
    main()
