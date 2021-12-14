# -*- coding:utf-8 -*-
"""
作者：Wcy
日期：2021年12月13日
时间：15:17:21
"""

import urllib.request as ur
import os
import easygui as e
import time


def url_open(url):
    time.sleep(0.1)
    req = ur.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/80.0.3987.116 Safari/537.36")

    response = ur.urlopen(req)
    html = response.read()

    return html


def find_next(html):
    a = html.find("url_next:", 0, -1)
    b = html.find(",", a, a+128)
    return html[a+10: b-1]


def find_title(html):
    a = html.find("mlfy_main_text")
    b = html.find("</h1>", a, a + 255)
    title = html[a + 24: b]
    return title


def find_content(html):
    content = []
    start = html.find("toolbarm();", 0, -1)
    end = html.find("铅笔小说", start, -1)

    a = html.find("<p>", start, end)
    while a < end:
        b = html.find("</p>", a, -1)
        if b < end:
            content.append(html[a + 3: b])
        else:
            break
        a = html.find("<p>", b + 3, -1)
    return content


def save_file(file_name, title, content_list):
    f = open(file_name, "a+", encoding="UTF-8")
    f.write(title + "\n\n")
    for content in content_list:
        f.write("    " + content + "\n\n")
    f.close()


if __name__ == "__main__":
    # html = url_open("https://www.23qb.net/book/191830/88120628.html").decode("gbk")
    url_next = "/book/191830/74610784.html"
    while url_next != "/book/191830/88120651.html":
        html = url_open("https://www.23qb.net" + url_next).decode("gbk")
        # 找到标题
        my_title = find_title(html)
        print(my_title)
        # 找到内容
        my_contents = find_content(html)
        # 保存成txt
        save_file("demo.txt", my_title, my_contents)
        print("保存完毕")
        # 找到下个网址
        url_next = find_next(html)
