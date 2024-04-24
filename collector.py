#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

import csv
import subprocess
import time
from random import random

from selenium import webdriver

# 开启tshark进行流量捕获
tshark_cmd = 'tshark -i WLAN -w wujiebantu.pcap'  # 运行前请修改网络接口与pcap文件名
tshark_process = subprocess.Popen(tshark_cmd, shell=True)

# 等待一段时间，确保tshark已经开始捕获流量
time.sleep(3)

# 设置浏览器选项
option = webdriver.EdgeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Edge(options=option)
# 使用Selenium控制Edge浏览器访问目标网页
with open('website.csv', 'r', encoding='utf-8') as file:  # 运行前请替换website.csv文件
    reader = csv.reader(file)
    for key, value in enumerate(reader):
        time.sleep(random() % 5 + 3)
        try:
            driver.get(value[0])
        except Exception as e:
            continue

# 关闭Edge浏览器
driver.quit()

# 停止tshark流量捕获
tshark_process.terminate()  # python中父进程结束，子进程不会自动结束，除非设置了守护进程
