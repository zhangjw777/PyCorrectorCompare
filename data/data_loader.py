# -*- coding: utf-8 -*-
"""
数据加载模块
"""

import json
import os
from typing import List, Dict, Optional


class DataLoader:
    """数据加载器"""
    
    def __init__(self, data_path: Optional[str] = None):
        """
        初始化数据加载器
        
        Args:
            data_path: 数据文件路径（可选）
        """
        self.data_path = data_path
        self.sentences: List[str] = []
    
    def load_from_file(self, file_path: str) -> List[str]:
        """
        从文件加载句子列表
        
        Args:
            file_path: 文件路径，支持 txt（每行一个句子）或 json 格式
            
        Returns:
            句子列表
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"数据文件不存在: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".txt":
            self.sentences = self._load_from_txt(file_path)
        elif ext == ".json":
            self.sentences = self._load_from_json(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
        
        return self.sentences
    
    def _load_from_txt(self, file_path: str) -> List[str]:
        """从txt文件加载，每行一个句子"""
        sentences = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    sentences.append(line)
        return sentences
    
    def _load_from_json(self, file_path: str) -> List[str]:
        """从json文件加载"""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 支持两种格式：
        # 1. 直接是句子列表 ["sentence1", "sentence2", ...]
        # 2. 字典格式 {"sentences": ["sentence1", "sentence2", ...]}
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "sentences" in data:
            return data["sentences"]
        else:
            raise ValueError("JSON格式不正确，应为列表或包含'sentences'键的字典")
    
    def load_from_list(self, sentences: List[str]) -> List[str]:
        """
        直接从列表加载句子
        
        Args:
            sentences: 句子列表
            
        Returns:
            句子列表
        """
        self.sentences = sentences
        return self.sentences
    
    def get_sentences(self) -> List[str]:
        """获取已加载的句子列表"""
        return self.sentences
    
    def __len__(self) -> int:
        """返回句子数量"""
        return len(self.sentences)
    
    def __iter__(self):
        """迭代器"""
        return iter(self.sentences)
