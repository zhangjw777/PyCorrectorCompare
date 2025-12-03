# -*- coding: utf-8 -*-
"""
评估指标计算模块

由于输入数据集全部是错误句子（正样本），评估逻辑如下：
- 如果模型检测到句子有错误 → True Positive (TP)
- 如果模型未检测到句子有错误 → False Negative (FN)

注意：由于没有负样本（正确句子），无法计算 FP 和 TN
因此这里的 Precision 在理论上为 100%（假设模型不会误报）
实际评估主要关注 Recall（召回率）
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class DetectionResult:
    """单个句子的检测结果"""
    sentence: str
    has_error_detected: bool  # 模型是否检测到错误
    corrected_sentence: str = ""  # 纠正后的句子（可选）
    error_details: List[Dict] = None  # 错误详情（可选）


class MetricsCalculator:
    """评估指标计算器"""
    
    def __init__(self):
        self.results: List[DetectionResult] = []
    
    def add_result(self, result: DetectionResult):
        """添加单个检测结果"""
        self.results.append(result)
    
    def add_results(self, results: List[DetectionResult]):
        """批量添加检测结果"""
        self.results.extend(results)
    
    def clear(self):
        """清空结果"""
        self.results = []
    
    def _count_tp_fn(self) -> Tuple[int, int]:
        """
        统计 TP 和 FN
        
        由于所有输入句子都是错误句子（正样本）：
        - TP: 模型正确检测到错误的句子数
        - FN: 模型未能检测到错误的句子数
        
        Returns:
            (TP, FN) 元组
        """
        tp = sum(1 for r in self.results if r.has_error_detected)
        fn = len(self.results) - tp
        return tp, fn
    
    def calculate_recall(self) -> float:
        """
        计算召回率 (Recall)
        
        Recall = TP / (TP + FN)
        在本场景下，所有样本都是正样本，因此：
        Recall = 检测到错误的句子数 / 总句子数
        """
        if len(self.results) == 0:
            return 0.0
        
        tp, fn = self._count_tp_fn()
        total = tp + fn
        
        if total == 0:
            return 0.0
        
        return tp / total
    
    def calculate_precision(self, fp: int = 0) -> float:
        """
        计算精确率 (Precision)
        
        Precision = TP / (TP + FP)
        
        注意：由于没有负样本，FP 需要外部提供（默认为0）
        如果 FP=0，则 Precision=1.0（假设所有检测结果都是正确的）
        
        Args:
            fp: False Positive 数量（可选，默认为0）
        """
        tp, _ = self._count_tp_fn()
        
        if tp + fp == 0:
            return 0.0
        
        return tp / (tp + fp)
    
    def calculate_f_score(self, beta: float, fp: int = 0) -> float:
        """
        计算 F-score
        
        F_beta = (1 + beta^2) * (Precision * Recall) / (beta^2 * Precision + Recall)
        
        Args:
            beta: F-score 的 beta 参数
                  - beta < 1: 更重视 Precision
                  - beta = 1: Precision 和 Recall 同等重要
                  - beta > 1: 更重视 Recall
            fp: False Positive 数量（默认为0）
        """
        precision = self.calculate_precision(fp)
        recall = self.calculate_recall()
        
        if precision + recall == 0:
            return 0.0
        
        beta_squared = beta ** 2
        f_score = (1 + beta_squared) * (precision * recall) / (beta_squared * precision + recall)
        
        return f_score
    
    def calculate_f05(self, fp: int = 0) -> float:
        """计算 F0.5 分数（更重视 Precision）"""
        return self.calculate_f_score(beta=0.5, fp=fp)
    
    def calculate_f1(self, fp: int = 0) -> float:
        """计算 F1 分数"""
        return self.calculate_f_score(beta=1.0, fp=fp)
    
    def calculate_f2(self, fp: int = 0) -> float:
        """计算 F2 分数（更重视 Recall）"""
        return self.calculate_f_score(beta=2.0, fp=fp)
    
    def calculate_all_metrics(self, fp: int = 0) -> Dict[str, float]:
        """
        计算所有评估指标
        
        Args:
            fp: False Positive 数量（默认为0）
            
        Returns:
            包含所有指标的字典
        """
        tp, fn = self._count_tp_fn()
        
        return {
            "total_sentences": len(self.results),
            "true_positive": tp,
            "false_negative": fn,
            "false_positive": fp,
            "precision": self.calculate_precision(fp),
            "recall": self.calculate_recall(),
            "f0.5": self.calculate_f05(fp),
            "f1": self.calculate_f1(fp),
            "f2": self.calculate_f2(fp),
        }
    
    def get_detailed_results(self) -> List[Dict]:
        """
        获取详细的检测结果
        
        Returns:
            每个句子的检测详情列表
        """
        detailed = []
        for i, result in enumerate(self.results):
            detailed.append({
                "index": i,
                "sentence": result.sentence,
                "detected": result.has_error_detected,
                "corrected": result.corrected_sentence,
                "details": result.error_details,
            })
        return detailed
    
    def print_summary(self, fp: int = 0):
        """打印评估摘要"""
        metrics = self.calculate_all_metrics(fp)
        
        print("=" * 50)
        print("评估结果摘要")
        print("=" * 50)
        print(f"总句子数: {metrics['total_sentences']}")
        print(f"检测到错误 (TP): {metrics['true_positive']}")
        print(f"未检测到错误 (FN): {metrics['false_negative']}")
        print(f"假阳性 (FP): {metrics['false_positive']}")
        print("-" * 50)
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F0.5: {metrics['f0.5']:.4f}")
        print(f"F1: {metrics['f1']:.4f}")
        print(f"F2: {metrics['f2']:.4f}")
        print("=" * 50)
