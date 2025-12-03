# -*- coding: utf-8 -*-
"""
MacBERT-CSC 纠错模型封装

使用 pycorrector 库中的 MacBERT-CSC 模型进行中文拼写纠错
"""

from typing import List, Dict, Optional
from .base_model import BaseCorrector, CorrectionResult


class MacBertCSCCorrector(BaseCorrector):
    """
    MacBERT-CSC 纠错模型
    
    基于 pycorrector 库的 MacBertCorrector
    """
    
    def __init__(self):
        """初始化 MacBERT-CSC 模型"""
        super().__init__(model_name="MacBERT-CSC")
        self._corrector = None
    
    def load_model(self):
        """
        加载 MacBERT-CSC 模型
        
        首次调用时会自动下载模型文件
        """
        if self._corrector is not None:
            return
        
        try:
            from pycorrector import MacBertCorrector
            self._corrector = MacBertCorrector("shibing624/macbert4csc-base-chinese")
            self._model = self._corrector  # 保持与基类一致
            print(f"[{self.model_name}] 模型加载成功")
        except ImportError as e:
            raise ImportError(
                f"无法导入 pycorrector 库，请先安装: pip install pycorrector\n"
                f"原始错误: {e}"
            )
        except Exception as e:
            raise RuntimeError(f"加载 {self.model_name} 模型失败: {e}")
    
    def correct(self, sentence: str) -> CorrectionResult:
        """
        对单个句子进行纠错
        
        Args:
            sentence: 输入句子
            
        Returns:
            CorrectionResult 对象，包含原始句子、纠正后句子、是否有错误、错误详情
        """
        if self._corrector is None:
            self.load_model()
        
        # 调用 pycorrector 的纠错方法
        # 返回格式: (corrected_text, [(wrong, correct, position), ...])
        corrected_text, error_details = self._corrector.correct(sentence)
        
        # 解析错误详情
        errors = self._parse_errors(error_details)
        
        # 判断是否检测到错误
        has_error = len(errors) > 0
        
        return CorrectionResult(
            original=sentence,
            corrected=corrected_text,
            has_error=has_error,
            errors=errors
        )
    
    def _parse_errors(self, error_details: List) -> List[Dict]:
        """
        解析错误详情
        
        Args:
            error_details: pycorrector 返回的错误详情列表
                          格式: [(wrong_char, correct_char, position), ...]
                          
        Returns:
            标准化的错误详情列表
        """
        errors = []
        for detail in error_details:
            if len(detail) >= 3:
                wrong_char, correct_char, position = detail[0], detail[1], detail[2]
                errors.append({
                    "position": position,
                    "original": wrong_char,
                    "corrected": correct_char,
                })
            elif len(detail) == 2:
                # 兼容某些版本可能只返回两个元素的情况
                wrong_char, correct_char = detail[0], detail[1]
                errors.append({
                    "position": -1,  # 位置未知
                    "original": wrong_char,
                    "corrected": correct_char,
                })
        return errors
    
    def correct_batch(self, sentences: List[str]) -> List[CorrectionResult]:
        """
        批量纠错
        
        Args:
            sentences: 句子列表
            
        Returns:
            CorrectionResult 列表
        """
        if self._corrector is None:
            self.load_model()
        
        results = []
        for sentence in sentences:
            result = self.correct(sentence)
            results.append(result)
        
        return results
