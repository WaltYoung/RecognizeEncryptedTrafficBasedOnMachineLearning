#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Xiao"
from collections import OrderedDict
import csv
from dataclasses import dataclass, field
from typing import Any, Final, Iterable, Optional
import ijson

MAX_PACKETLEN = 30

websites_mapper: Final[dict[str, str]] = {
    "52pojie": "www.52pojie.cn",
    "cnki": "www.cnki.net",
    "wzu": "www.wzu.edu.cn",
    "12371": "www.12371.cn",
    "ghxi": "www.ghxi.com",
    "runoob": "www.runoob.com",
    "freesion": "www.freesion.com",
    "ccf": "www.ccf.org.cn",
    "chinaz": "tool.chinaz.com",
    "yiz": "www.yiz.vip",
    "wujiebantu": "www.wujiebantu.com",
}

target: Final[str] = "52pojie"  # 运行前请修改目标文件名
pcap_file_path: Final[str] = f"{target}.pcap"
json_file_path: Final[str] = f"{target}.json"


@dataclass
class Stream:
    tcp_stream: str
    sni: Optional[str] = None
    tcp_length: list[int] = field(default_factory=list)


def main():
    # 创建类的实例数组
    streams: OrderedDict[str, Stream] = OrderedDict()

    # 读取JSON数据文件
    with open(json_file_path, "rb") as f:
        # 使用ijson.parse方法解析JSON数据
        data: Iterable[tuple[Iterable[str] | str, Any, str]] = ijson.parse(f)

        # 遍历解析出的数据
        cur_tcp_stream: str = "0"
        cur_frame_protocols: str = ""
        for prefix, _, value in data:
            # 检查特定字段的前缀并提取数据
            if "frame.protocols" in prefix:
                cur_frame_protocols = value

            if "tcp.stream" in prefix:
                if "tcp:tls" in cur_frame_protocols:
                    cur_tcp_stream = value
                    streams.setdefault(value, Stream(value))

            if "tls.handshake.extensions_server_name" in prefix:
                if "tcp:tls" in cur_frame_protocols:
                    if not value.isdigit():
                        if cur_tcp_stream in streams:
                            if streams[cur_tcp_stream].sni is None:
                                streams[cur_tcp_stream].sni = value

            if "tcp.payload" in prefix:
                if "tcp:tls" in cur_frame_protocols:
                    length = value.count(":") + 1
                    if cur_tcp_stream in streams:
                        streams[cur_tcp_stream].tcp_length.append(length)

        for stream in streams.values():
            stream.tcp_length = (stream.tcp_length + [0] * MAX_PACKETLEN)[
                :MAX_PACKETLEN
            ]

    with open("dataset.csv", "a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(
            (
                (
                    websites_mapper[target],
                    pcap_file_path,
                    stream.tcp_stream,
                    stream.sni if stream.sni is not None else "",
                    *stream.tcp_length,
                )
                for stream in streams.values()
            )
        )


if __name__ == "__main__":
    main()
