import requests
from urllib.parse import urlencode
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
        self._tag_url = self.structure_url(self._keywords, start_date, end_date, self._area)
        self.get_result(self._tag_url)

    def get_result(self, tag_url):
        for start_date, end_date in self._time_range_list:
            encrypt_datas, uniqid = self.get_encrypt_datas(start_date, end_date, tag_url)
            key = self.get_key(uniqid)
            for encrypt_data in encrypt_datas:
                for kind in self._all_kind:
                    encrypt_data[kind]['data'] = self.decrypt_func(key, encrypt_data[kind]['data'])
                self.format_data(encrypt_data)

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
        html = self.http_get(tag_url)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def get_key(self, uniqid):
        tag_url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self.http_get(tag_url)
        datas = json.loads(html)
        key = datas['data']
        return key

    def format_data(self, data):
        keyword = str(data['word'])
        time_len = len(data['all']['data'])
        start_date = data['all']['startDate']
        cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(time_len):
            for kind in self._all_kind:
                index_datas = data[kind]['data']
                index_data = index_datas[i] if len(index_datas) != 1 else index_datas[0]
                formated_data = {
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'index': index_data if index_data else '0'
                }
                self.result[keyword][kind].append(formated_data)
            cur_date += datetime.timedelta(days=1)

    def __call__(self, keyword, kind='all'):
        return self.result[keyword][kind]

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
                date_range_list.append((startdate, enddate))
                return date_range_list
            date_range_list.append((startdate, tempdate))
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

    @staticmethod
    def structure_url(keyword, startdate, enddate, area):
        # 这里暂时是一个单独url的测试，后续应该返回的是一个目标url的集合
        request_args = {
            'word': ','.join(keyword),
            'startDate': startdate,
            'endDate': enddate,
            'area': area,
        }
        tag_url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        return tag_url


class Tag:
    def __init__(self):
        pass

def main():
    # 设定几个需要获取指数的url并逐个进行数据爬取，最后再进行封装存储成excel文件
    pass


if __name__ == '__main__':
    bi = BaiduIndex('股票', '2019-06-25', '2019-07-24', 189)
    res = bi.result['股票']
    print(res['pc'])