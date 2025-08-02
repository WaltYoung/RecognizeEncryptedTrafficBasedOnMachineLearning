#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Xiao"

import subprocess

# 开启tshark进行流量分析
target = "52pojie"  # 运行前请修改目标文件名
pcap_file_path = target + ".pcap"
json_file_path = target + ".json"
tshark_cmd = "tshark -r " + pcap_file_path + " -V -T json >> " + json_file_path
tshark_process = subprocess.Popen(tshark_cmd, shell=True)

# tshark_process.terminate()
