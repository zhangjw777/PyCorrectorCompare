# -*- coding: utf-8 -*-
"""
纠错模型基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CorrectionResult:
    """单个句子的纠错结果"""
    original: str  # 原始句子
    corrected: str  # 纠正后的句子
    has_error: bool  # 是否检测到错误
    errors: List[Dict]  # 错误详情列表，每个错误包含位置、原字符、纠正字符等


class BaseCorrector(ABC):
    """纠错模型基类"""
    
    def __init__(self, model_name: str):
        """
        初始化纠错模型
        
        Args:
            model_name: 模型名称
        """
        self.model_name = model_name
        self._model = None
    
    @abstractmethod
    def load_model(self):
        """加载模型"""
        pass
    
    @abstractmethod
    def correct(self, sentence: str) -> CorrectionResult:
        """
        对单个句子进行纠错
        
        Args:
            sentence: 输入句子
            
        Returns:
            CorrectionResult 对象
        """
        pass
    
    def correct_batch(self, sentences: List[str]) -> List[CorrectionResult]:
        """
        批量纠错
        
        Args:
            sentences: 句子列表
            
        Returns:
            CorrectionResult 列表
        """
        results = []
        for sentence in sentences:
            result = self.correct(sentence)
            results.append(result)
        return results
    
    def detect_error(self, sentence: str) -> bool:
        """
        检测句子是否有错误
        
        Args:
            sentence: 输入句子
            
        Returns:
            是否检测到错误
        """
        result = self.correct(sentence)
        return result.has_error
    
    def detect_batch(self, sentences: List[str]) -> List[bool]:
        """
        批量检测错误
        
        Args:
            sentences: 句子列表
            
        Returns:
            布尔值列表，表示每个句子是否有错误
        """
        return [self.detect_error(s) for s in sentences]
    
    def get_model_name(self) -> str:
        """获取模型名称"""
        return self.model_name
    
    def is_loaded(self) -> bool:
        """检查模型是否已加载"""
        return self._model is not None
