#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Xiao"

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

if __name__ == "__main__":
    TRAINPATH = "train.csv"
    TESTPATH = "predict.csv"

    train_df = pd.read_csv(TRAINPATH)
    test_df = pd.read_csv(TESTPATH)

    combined_data = pd.concat([train_df, test_df], axis=0)  # 合并训练数据和测试数据
    combined_data_encoded = pd.get_dummies(
        combined_data, columns=["sni"]
    )  # 对合并后的数据进行独热编码

    train_data_encoded = combined_data_encoded.iloc[: len(train_df), :]
    test_data_encoded = combined_data_encoded.iloc[len(train_df) :, :]

    train_label = train_data_encoded.iloc[:, 0]
    train_data_encoded = train_data_encoded.iloc[:, 2:]

    test_label = test_data_encoded.iloc[:, 0]
    test_data_encoded = test_data_encoded.iloc[:, 2:]

    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(train_data_encoded, train_label)
    y_pred = rf_classifier.predict(test_data_encoded)
    accuracy = accuracy_score(test_label, y_pred)
    precision = precision_score(test_label, y_pred, average="weighted")
    recall = recall_score(test_label, y_pred, average="weighted")
    f1 = f1_score(test_label, y_pred, average="weighted")

    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")

    labels = ["Accuracy", "Precision", "Recall", "F1 Score"]
    values = [accuracy, precision, recall, f1]

    plt.bar(labels, values, color=["red", "blue", "green", "orange"])
    plt.ylim(0, 1)  # 设置y轴范围为0到1
    plt.ylabel("Score")
    plt.title("Evaluation Metrics")
    plt.show()
