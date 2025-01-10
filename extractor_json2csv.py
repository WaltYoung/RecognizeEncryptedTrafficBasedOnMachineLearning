#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

import ijson

MAX_PACKETLEN = 30

dictionary = {
    '52pojie': 'www.52pojie.cn',
    'cnki': 'www.cnki.net',
    'wzu': 'www.wzu.edu.cn',
    '12371': 'www.12371.cn',
    'ghxi': 'www.ghxi.com',
    'runoob': 'www.runoob.com',
    'freesion': 'www.freesion.com',
    'ccf': 'www.ccf.org.cn',
    'chinaz': 'tool.chinaz.com',
    'yiz': 'www.yiz.vip',
    'wujiebantu': 'www.wujiebantu.com'
}

target = '52pojie'  # 运行前请修改目标文件名
pcap_file_path = target + '.pcap'
json_file_path = target + '.json'


class Stream:
    def __init__(self, tcp_stream, sni, length):
        self.tcp_stream = tcp_stream
        self.sni = sni
        self.tcp_length = length


# 创建类的实例数组
streams = []


def insertSNI(cur_tcp_stream, value):
    for stream in streams:
        if stream.tcp_stream == cur_tcp_stream:
            if stream.sni is None:
                stream.sni = value


def appendLength(cur_tcp_stream, value):
    for stream in streams:
        if stream.tcp_stream == cur_tcp_stream:
            if stream.tcp_length is None:
                stream.tcp_length = value
            else:
                stream.tcp_length += ',' + value


def removeLength(cur_tcp_stream, input_string, max_packetlen):
    for stream in streams:
        if stream.tcp_stream == cur_tcp_stream:
            comma_count = 0
            index = 0
            for i, char in enumerate(input_string):
                if char == ',':
                    comma_count += 1
                    if comma_count == max_packetlen:
                        index = i
                        break
            stream.tcp_length = input_string[:index]


if __name__ == '__main__':
    # 读取JSON数据文件
    with open(json_file_path, 'rb') as f:
        # 使用ijson.parse方法解析JSON数据
        data = ijson.parse(f)

        # 遍历解析出的数据
        cur_tcp_stream = '0'
        cur_frame_protocols = ''
        for prefix, event, value in data:
            # 检查特定字段的前缀并提取数据
            if 'frame.protocols' in prefix:
                cur_frame_protocols = value

            if 'tcp.stream' in prefix:
                if 'tcp:tls' in cur_frame_protocols:
                    cur_tcp_stream = value
                    if all(stream.tcp_stream != value for stream in streams): # 检查是否存在以value为key的stream
                        streams.append(Stream(value, None, None))

            if 'tls.handshake.extensions_server_name' in prefix:
                if 'tcp:tls' in cur_frame_protocols:
                    if not value.isdigit():
                        insertSNI(cur_tcp_stream, value)

            if 'tcp.payload' in prefix:
                if 'tcp:tls' in cur_frame_protocols:
                    length = str(value).count(':') + 1
                    appendLength(cur_tcp_stream, str(length))

        for stream in streams:
            count = str(stream.tcp_length).count(',') + 1
            if count < MAX_PACKETLEN:
                for i in range(MAX_PACKETLEN - count):
                    appendLength(stream.tcp_stream, '0')
            elif count > MAX_PACKETLEN:
                removeLength(stream.tcp_stream, stream.tcp_length, MAX_PACKETLEN)

    with open('dataset.csv', 'a', encoding='utf-8', newline='') as csv_file:
        for stream in streams:
            if stream.sni is None:
                stream.sni = ''
            csv_file.write(dictionary[target] + ',' + pcap_file_path + ',' + stream.tcp_stream + ',' + stream.sni + ',' + stream.tcp_length + '\n')
