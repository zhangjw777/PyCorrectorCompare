# PyCorrectorCompare

使用 pycorrector 库中的纠错模型对错误句子数据集进行检错评估，用于与自研模型进行对比。

## 项目结构

```
PyCorrectorCompare/
├── config/                 # 配置模块
│   ├── __init__.py
│   └── settings.py         # 项目配置
├── data/                   # 数据模块
│   ├── __init__.py
│   └── data_loader.py      # 数据加载器
├── docs/                   # 文档
│   └── 项目修改计划.md      # 修改计划与记录
├── evaluation/             # 评估模块
│   ├── __init__.py
│   └── metrics.py          # 评估指标计算
├── models/                 # 模型模块
│   ├── __init__.py
│   ├── base_model.py       # 模型基类
│   └── macbert_csc.py      # MacBERT-CSC 模型封装
├── output/                 # 输出目录（运行时生成）
│   └── results/            # 评估结果
├── main.py                 # 主运行脚本
├── run_macbert_csc.py      # MacBERT-CSC 专用脚本
├── requirements.txt        # 依赖包
└── README.md
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：直接在代码中填入数据

编辑 `run_macbert_csc.py`，在 `ERROR_SENTENCES` 列表中填入错误句子：

```python
ERROR_SENTENCES = [
    "今天天汽很好",
    "我门一起去公园",
    # ... 更多句子
]
```

然后运行：

```bash
python run_macbert_csc.py
```

### 方法二：从文件加载数据

支持 `.txt`（每行一个句子）或 `.json` 格式：

```bash
python run_macbert_csc.py --file data/error_sentences.txt
```

## 评估指标

- **Precision**（精确率）
- **Recall**（召回率）
- **F0.5**（更重视 Precision）
- **F1**
- **F2**（更重视 Recall）

## 输出结果

结果保存在 `output/results/` 目录下，包含：
- 评估指标汇总
- 每个句子的检测详情

## 支持的模型

- [x] MacBERT-CSC
- [ ] 其他模型（待添加）

## 注意事项

1. 输入数据集应全部为错误句子（正样本）
2. 评估重点关注模型能否正确检测出句子存在错误
3. 首次运行时会自动下载模型文件
