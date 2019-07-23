import requests
from collections import defaultdict
import datetime
import requests
import json
import pandas as pd


COOKIE = ''

headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttoRequest',
    'User-Agent': (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    )

}

class BaiduIndex:
    def __init__(self, keywords, start_date, end_date, area=0):
        """
        初始化BaiduIndex对象，赋予一些基本属性
        :param keywords: 关键词
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param area: 区域，默认0代表全国（地区代码需要自己总结）
        """
        self._keywords = keywords if isinstance(keywords, list) else keywords.split(',')
        self._time_range_list = self.get_time_rangew_list(start_date, end_date)
        self._all_kind = ['all', 'pc', 'wise']
        self._area = area
        self.result = {keyword: defaultdict(list) for keyword in self._keywords}

if __name__ == '__main__':
    print(headers['User-Agent'])
