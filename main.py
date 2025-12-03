# -*- coding: utf-8 -*-
"""
主运行脚本

使用 pycorrector 中的模型对错误句子数据集进行检错评估
"""

import json
import os
from datetime import datetime
from typing import List, Dict

from data.data_loader import DataLoader
from models.macbert_csc import MacBertCSCCorrector
from evaluation.metrics import MetricsCalculator, DetectionResult
from config.settings import OUTPUT_DIR, RESULTS_DIR


def ensure_output_dirs():
    """确保输出目录存在"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)


def run_evaluation(
    sentences: List[str],
    model_name: str = "macbert_csc",
    save_results: bool = True,
    verbose: bool = True
) -> Dict:
    """
    运行评估流程
    
    Args:
        sentences: 错误句子列表（全部为正样本）
        model_name: 使用的模型名称
        save_results: 是否保存结果到文件
        verbose: 是否打印详细信息
        
    Returns:
        评估结果字典
    """
    ensure_output_dirs()
    
    # 选择模型
    if model_name == "macbert_csc":
        corrector = MacBertCSCCorrector()
    else:
        raise ValueError(f"不支持的模型: {model_name}")
    
    if verbose:
        print(f"正在加载模型: {corrector.get_model_name()}")
    
    # 加载模型
    corrector.load_model()
    
    if verbose:
        print(f"开始对 {len(sentences)} 个句子进行检错...")
    
    # 进行纠错并收集结果
    calculator = MetricsCalculator()
    detailed_results = []
    
    for i, sentence in enumerate(sentences):
        result = corrector.correct(sentence)
        
        # 添加到评估计算器
        detection_result = DetectionResult(
            sentence=sentence,
            has_error_detected=result.has_error,
            corrected_sentence=result.corrected,
            error_details=result.errors
        )
        calculator.add_result(detection_result)
        
        # 记录详细结果
        detailed_results.append({
            "index": i,
            "original": sentence,
            "corrected": result.corrected,
            "detected": result.has_error,
            "errors": result.errors
        })
        
        # 进度提示
        if verbose and (i + 1) % 100 == 0:
            print(f"已处理: {i + 1}/{len(sentences)}")
    
    # 计算指标
    metrics = calculator.calculate_all_metrics()
    
    # 打印摘要
    if verbose:
        calculator.print_summary()
    
    # 构建完整结果
    full_results = {
        "model_name": corrector.get_model_name(),
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics,
        "detailed_results": detailed_results
    }
    
    # 保存结果
    if save_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = os.path.join(RESULTS_DIR, f"{model_name}_results_{timestamp}.json")
        
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(full_results, f, ensure_ascii=False, indent=2)
        
        if verbose:
            print(f"结果已保存到: {result_file}")
    
    return full_results


def main():
    from datasets import load_dataset
    ds = load_dataset("shibing624/chinese_text_correction")
    datas = ds['train'][0:1000]
    """主函数"""
    # ===================================
    # 在这里填入错误句子列表
    # ===================================
    error_sentences = [
        # TODO: 在这里添加你的错误句子列表
        # 示例：
        # "今天天汽很好",
        # "我门一起去公园",
        # "这个问提很难",
    ]
    error_sentences = [src for src, label in zip(datas['source'], datas['type']) if label == 'negative']
    
    if not error_sentences:
        print("警告: 错误句子列表为空，请在 main.py 中填入数据")
        print("或使用 DataLoader 从文件加载数据")
        return
    
    # 运行评估
    results = run_evaluation(
        sentences=error_sentences,
        model_name="macbert_csc",
        save_results=True,
        verbose=True
    )
    
    return results


if __name__ == "__main__":
    main()
