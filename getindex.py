import requests
from collections import defaultdict
import datetime
import requests
import json
# import pandas as pd


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
        self._time_range_list = self.get_time_range_list(start_date, end_date)
        self._all_kind = ['all', 'pc', 'wise']
        self._area = area
        self.result = {keyword: defaultdict(list) for keyword in self._keywords}

    # def get_result(self):
    #     for start_date, end_date in self._time_range_list:
    #         encrypt_datas, uniqid = self.get_encrypt

    def get_encrypt_datas(self, start_date, end_date, tag_url):
        """
        获取加密的数据
        :param start_date: 格式化后的开始日期
        :param end_date: 格式化后的结束日期
        :param tag_url: 需要访问的目标url
        :return: 加密的结果数据
        """
        request_args = {
            'word': ','.join(self._keywords),
            'startDate': start_date,
            'endDate': end_date,
            'area': self._area,
        }
        # 获取页面数据
        html = self.http_get(url)

    @staticmethod
    def http_get(url):
        # 获取已经存储好的cookie
        with open('cookies', 'r') as f:
            cookies = f.read()
        headers['Cookie'] = cookies
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @staticmethod
    def get_time_range_list(startdate, enddate):
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            tempdate = startdate + datetime.timedelta(days=300)
            if tempdate > enddate:
                all_days = (enddate-startdate).days  # 还不知道有神马用
                date_range_list.append(startdate, enddate)
                return date_range_list
            date_range_list.append(startdate, tempdate)
            startdate = tempdate + datetime.timedelta(days=1)

    @staticmethod
    def decrypt_func(key, data):
        """
        decrypt data
        """
        a = key
        i = data
        n = {}
        s = []
        for o in range(len(a) // 2):
            n[a[o]] = a[len(a) // 2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')





if __name__ == '__main__':
    key = 'uVvS.HO,D3mhUJM0128%74.-3+95,6'
    data = 'VMOuVJVH3SOJVUOvUJVUM3uJVOV3SJOMUUJOuMvJVhH3UJVSM3HJVMU3VJVMHUHJV3HUUJOV3hJ3MuUJVhOOuJVMSHvJVUuOuJVUVhOJVVSVvJ3MuVJvhOUJVOSvuJV3v3VJVvS3MJVV3UhJVuUUhJ3HuOJ3u3MJVUM3vJVvVhM'
    res = BaiduIndex.decrypt_func(key, data)
    print(res)