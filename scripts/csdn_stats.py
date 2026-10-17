# -*- coding: utf-8 -*-
"""抓取 CSDN 个人主页的统计数据，写入 csdn.json（供 shields.io 动态徽章读取）"""
import json
import re
import sys
import urllib.request

USER = "Sakura_j_h_"
URL = "https://blog.csdn.net/" + USER
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9",
}

MAPPING = {"总访问量": "views", "原创": "original", "粉丝": "fans", "关注": "following"}
PATTERN = (
    r'user-profile-statistics-num[^>]*>([^<]+)</div>\s*'
    r'<div class="user-profile-statistics-name"[^>]*>([^<]+)</div>'
)


def main():
    req = urllib.request.Request(URL, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

    data = {}
    for num, name in re.findall(PATTERN, html):
        key = MAPPING.get(name.strip())
        if key:
            data[key] = int(num.strip().replace(",", ""))

    if "views" not in data:
        print("解析失败：没有找到「总访问量」，CSDN 页面结构可能变了", file=sys.stderr)
        sys.exit(1)

    data["user"] = USER
    data["source"] = URL

    with io_open() as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(json.dumps(data, ensure_ascii=False))


def io_open():
    import io
    return io.open("csdn.json", "w", encoding="utf-8")


if __name__ == "__main__":
    main()
