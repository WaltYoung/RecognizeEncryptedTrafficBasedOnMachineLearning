#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Xiao"

import pandas as pd
from sklearn.model_selection import train_test_split

# 读取原始数据集，假设数据集保存为 data.csv
data = pd.read_csv("dataset.csv")

# 按7:3的比例随机切分数据集
train_data, predict_data = train_test_split(data, test_size=0.3)

# 保存训练集到 train.csv
train_data.to_csv("train.csv", index=False)

# 保存预测集到 predict.csv
predict_data.to_csv("predict.csv", index=False)
