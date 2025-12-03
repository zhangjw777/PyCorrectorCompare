# -*- coding: utf-8 -*-
"""
项目配置文件
"""

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据目录
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# 结果输出目录
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results")

# 模型配置
MODEL_CONFIGS = {
    "macbert_csc": {
        "name": "MacBERT-CSC",
        "description": "基于MacBERT的中文拼写纠错模型",
    },
    # 后续可添加更多模型配置
}

# 评估配置
EVALUATION_CONFIG = {
    "metrics": ["precision", "recall", "f0.5", "f1", "f2"],
}
