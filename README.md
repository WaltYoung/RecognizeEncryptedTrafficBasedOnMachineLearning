# 基于机器学习的加密流量识别

## 加密流量定向生成

环境：Python3 + Selenium + Edge + Edge Driver

### Edge Driver配置教程

下载Edge浏览器对应版本的驱动器*（Edge浏览器的版本可在设置中查询得到）*

Edge Driver下载地址：[https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads)

将下载的`Edge Driver`重命名为`MicrosoftWebDriver.exe`，复制驱动器到浏览器可执行程序的目录`C:\Program Files (x86)\Microsoft\Edge`

### Python环境配置教程

pycharm首次打开本项目，将自动下载依赖项，如没有，请在终端中运行`pip install -r requirements.txt`

### 程序简介

本程序使用编程化、爬虫化方式收集网页链接，并以csv文件格式进行存储。网页存储的格式为网站名称，网页链接。

1. 遍历各种元素列表，如果元素具有有效的href或src属性，则将标题和链接/源属性写入CSV文件中。
2. 对于`<a>`元素，检查链接是否为空的JavaScript脚本，如果是，则跳过写入操作。
3. 以追加模式打开CSV文件links.csv，并写入数据。

### 运行步骤

1. 新建`links.csv`文件
2. 替换`generator.py`文件第12行的网址为你想要爬取的网站网址。
3. 运行`generator.py`文件，静待程序运行完成。程序运行完成后将自动关闭Edge浏览器。
4. 可在`links.csv`文件中找到爬取的链接。

## 加密流量定向采集

环境：Python3 + Selenium + Edge + Edge Driver + Wireshark

### 程序简介

本程序通过Python编程结合Selenium和tshark，实现对特定网站的流量采集。程序首先通过Python的subprocess库启动tshark进行流量捕获，然后使用Selenium控制Edge访问目标网页，同时捕获网络流量。用户可以指定需要监控的网络接口和其他参数，实现对网络流量的自动化捕获。

1. 使用Tshark实现命令行下的流量采集：选项`-i`后接网络接口的名称；选项`-w`后接输出的文件名
2. 设置浏览器选项：创建EdgeOptions对象，为其添加了一个选项，该选项的键是detach，值为True。这个特定选项允许浏览器在脚本执行完毕后保持打开状态。使用之前配置好的EdgeOptions对象来创建一个Microsoft Edge浏览器的WebDriver实例。
3. 读取csv文件：必须指定使用`utf-8`编解码，**csv文件不默认使用utf-8编码，故需要使用记事本另存为csv文件使用utf-8编码**
4. 随机等待：因为短时间频繁请求网站资源，可能会被网站拦截或遇到如429等错误，故在打开下一个链接前需等待一段随机时间
5. 错误处理：因为采集流量时会遇到预期以外的错误，故需要进行错误处理增强代码的鲁棒性，避免Selenium因错误而异常退出
6. 结束子进程：完成该网站的流量采集后关闭Edge浏览器，停止tshark流量捕获

### 运行步骤

1. 修改tshark命令，即网络接口与pcap文件名
2. 运行前请替换上一步得到`website.csv`文件
3. 运行`collector.py`文件，静待程序运行完成。程序运行完成后将自动关闭Edge浏览器。
4. 在pycharm的项目目录中可以找到相应的pcap文件。
5. 如有需要，可在修改tshark命令后多次执行1-4步以得到多个流量文件

## 加密流量特征提取

环境：Python3 + ijson + Tshark

### 程序简介

本程序使用`ijson`库进行json文件解析和处理，能够从pcap文件中提取网络流特征，用于加密流量行为识别。

本程序由2个python文件`extractor_pcap2json.py`和`extractor_ json2csv.py`组成。

1. `extractor_pcap2json.py`利用tshark组件对流量进行分析，将流量文件转换为JSON文件，方便解析读取。
2. `extractor_json2csv.py`利用ijson库逐行读入大型json文件以避免内存不够的问题。


### 运行步骤

1. 修改目标文件名
2. 运行`extractor_pcap2json.py`，将在当前目录下得到与流量文件同名的json文件。**请等待json文件大小不再改变**，文件大小不再改变时表明子进程结束
3. 修改目标文件名和文件对应的域名，将目标文件名修改为第二步得到的流量文件名，并在字典中补充流量文件名对应的域名。
4. 运行`extractor_json2csv.py`，将在当前目录下得到名为`dataset.csv`文件
5. 如有需要，可在修改目标文件名和文件对应的域名后多次执行1-4步以得到汇总的数据集
6. `dataset.csv`文件字段顺序：域名，流量文件的文件名，流号，SNI字段，包长1，包长2，包长3，…，包长30


## 加密流量识别

环境：Python3 + scikit-learn

### 程序简介

本程序使用`scikit-learn`库中的随机森林的机器学习方法进行加密流量识别。

本程序由2个python文件`splitter.py`和`recognizer.py`组成。

1. `splitter.py`利用`sklearn`库中的`train_test_split`方法对数据集进行切分。
2. `recognizer.py`利用`sklearn`库中的随机森林进行加密流量识别。

### 运行步骤

本程序应首先运行`splitter.py`，再运行`recognizer.py`组成。2个python文件已经解耦。

1. 修改各个参数：在`splitter.py`文件中，第10行修改为数据集文件的文件名；第13行修改为你希望的数据集切分比例；第16行修改为希望保存的训练集的文件名；第19行修改为希望保存的预测集的文件名。并为数据集文件每列添加列名。
2. **为上一步得到的`dataset.csv`的每一列添加列名**，`dataset.csv`文件字段顺序：域名，流量文件的文件名，流号，SNI字段，包长1，包长2，包长3，…，包长30。**建议使用英文**，尽量避免使用汉字，并且**建议SNI字段的列名为sni**
3. 运行`splitter.py`，将在当前目录下得到与训练集和预测集的csv文件。
4. 修改各个参数：在`recognizer.py`文件中，第12行修改为训练集的文件名，第13行修改为预测集的文件名，如在第一步中未修改已有的文件名，则此处不需要修改；第19行修改为你所使用训练集和预测集的SNI字段的列名，如在第二步中遵循建议，将SNI字段的列名定为sni，则此处不需要修改；第30行修改为希望使用的决策树数量与随机数。*中型数据库推荐决策树数量在[500,1000]区间*
5. 运行`recognizer.py`，将在终端得到**Accuracy、Precision、Recall、F1 Score**四项评价指标的具体值，可在弹出的页面看到四项评价指标的**图形化展示**。