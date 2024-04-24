#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

import csv

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge()
driver.get(r'https://www.cnki.net/')

# for item in cookies: # 若网页需要cookies
#     driver.add_cookie(item)

# links = driver.find_elements_by_tag_name('link') # 旧版本代码
links = driver.find_elements(By.TAG_NAME, "link")  # 新版本代码
scripts = driver.find_elements(By.TAG_NAME, "script")
a = driver.find_elements(By.TAG_NAME, "a")
img = driver.find_elements(By.TAG_NAME, "img")

with open('links.csv', 'a', newline='') as file:  # a表示追加
    writer = csv.writer(file)
    # writer.writerow(['Link Text', 'URL'])
    for link in links:
        if link.get_attribute('href') is None:
            continue
        writer.writerow([driver.title, link.get_attribute('href')])
    for link in scripts:
        if link.get_attribute('href') is None:
            continue
        writer.writerow([driver.title, link.get_attribute('src')])
    for link in a:
        if link.get_attribute('href') is not None and "javascript:" in link.get_attribute('href'):
            continue
        elif link.get_attribute('href') is None:
            continue
        writer.writerow([driver.title, link.get_attribute('href')])
    for link in img:
        writer.writerow([driver.title, link.get_attribute('src')])
