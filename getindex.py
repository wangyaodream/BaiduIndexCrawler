from urllib.parse import urlencode
from collections import defaultdict
from tag import Tag
import random
import os
import threading
import time
import datetime
import requests
import json

import datapack

import datapack as dp
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


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class BaiduIndex:
    def __init__(self, cookie, tag_url, keywords, start_date, end_date, area=0):
        """
        初始化BaiduIndex对象，赋予一些基本属性
        :param keywords: 关键词
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param area: 区域，默认0代表全国（地区代码需要自己总结）
        """
        self._cookie = cookie
        self._keywords = keywords if isinstance(keywords, list) else keywords.split(',')
        self._time_range_list = self.get_time_range_list(start_date, end_date)
        self._all_kind = ['all', 'pc', 'wise']
        self._area = area
        self.result = {keyword: defaultdict(list) for keyword in self._keywords}
        self.get_result(tag_url)

    def get_result(self, tag_url):
        for start_date, end_date in self._time_range_list:
            encrypt_datas, uniqid = self.get_encrypt_datas(start_date, end_date, tag_url)
            key = self.get_key(uniqid)
            if 'all' in encrypt_datas[0]:
                for encrypt_data in encrypt_datas:
                    for kind in self._all_kind:
                        encrypt_data[kind]['data'] = self.decrypt_func(key, encrypt_data[kind]['data'])
                    self.format_data(encrypt_data)
            else:
                for encrypt_data in encrypt_datas:
                    encrypt_data['data'] = self.decrypt_func(key, encrypt_data['data'])
                self.format_data(encrypt_data, specific=False)

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
        html = self.http_get(tag_url, self._cookie)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        if 'userIndexes' in datas['data']:
            for single_data in datas['data']['userIndexes']:
                encrypt_datas.append(single_data)
        else:
            for single_data in datas['data']['index']:
                encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def get_key(self, uniqid):
        tag_url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self.http_get(tag_url, self._cookie)
        datas = json.loads(html)
        key = datas['data']
        return key

    def format_data(self, data, specific=True):

        if specific:
            time_len = len(data['all']['data'])
            keyword = str(data['word'])
            start_date = data['all']['startDate']
        else:
            time_len = len(data['data'])
            keyword = str(data['key'])
            start_date = data['startDate']

        cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(time_len):
            if specific:
                for kind in self._all_kind:
                    index_datas = data[kind]['data']
                    index_data = index_datas[i] if len(index_datas) != 1 else index_datas[0]
                    formated_data = {
                        'date': cur_date.strftime('%Y-%m-%d'),
                        'index': index_data if index_data else '0'
                    }
                    self.result[keyword][kind].append(formated_data)
            else:
                index_datas = data['data']
                index_data = index_datas[i] if len(index_datas) != 1 else index_datas[0]
                formated_data = {
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'index': index_data if index_data else '0'
                }
                self.result[keyword]['all'].append(formated_data)
            cur_date += datetime.timedelta(days=1)

    def __call__(self, keyword, kind='all'):
        return self.result[keyword][kind]

    @staticmethod
    def http_get(url, cookie):
        # 获取已经存储好的cookie
        headers['Cookie'] = cookie
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


def getNationalData(cookie, keyword, startDate, endDate, targ: Tag):
    # 获取全国的数据
    url = targ.structure_urls(keyword, startDate, endDate, 0)
    result_data = {}
    bi = BaiduIndex(cookie, url, [keyword], startDate, endDate, 0)
    result_data = dict(bi.result[keyword])
    return result_data


def getProvinceData(cookie, keyword, startDate, endDate, provinceMap, targ: Tag):
    result_data = {}
    out_thread = []
    thread_list = []
    for curr_province in provinceMap:
        # time.sleep(0.1)

        province_name = curr_province
        province_code = provinceMap[curr_province]
        _url = targ.structure_urls(keyword, startDate, endDate, province_code)
        # 单线程
        bi = BaiduIndex(cookie, _url, [keyword], startDate, endDate, province_code)
        temp_data = dict(bi.result[keyword])

        #     # 多线程
        #     t = MyThread(BaiduIndex, args=(cookie, _urls[i], [keyword], startDate, endDate, province_code))
        #     thread_list.append((i, t))
        #     t.start()
        # for item_name, t in thread_list:
        #     t.join()
        #     res = t.get_result()
        #     temp_data[item_name] = dict(res.result[keyword])
        result_data[province_name] = temp_data
    return result_data


def getCitysData(cookie, keyword, startDate, endDate, citysMap, targ: Tag):
    result_data = {}
    citys_data = {}
    for i in citysMap:
        citys_data.update(citysMap[i])
    for city in citys_data:
        thread_list = []
        city_code = citys_data[city]
        _url = targ.structure_urls(keyword, startDate, endDate, city_code)
        # 单线程
        bi = BaiduIndex(cookie, _url, [keyword], startDate, endDate, city_code)
        temp_data = dict(bi.result[keyword])

        #     # 多线程
        #     t = MyThread(BaiduIndex, args=(cookie, _urls[i], [keyword], startDate, endDate, city_code))
        #     thread_list.append((i, t))
        #     t.start()
        # for item_name, t in thread_list:
        #     t.join()
        #     res = t.get_result()
        #     if res:
        #         temp_data[item_name] = dict(res.result[keyword])
        result_data[city] = temp_data
    return result_data

def main(keyword, startDate, endDate, target, target_path='.'):
    target_dirs = {
        'SearchIndex': '搜索指数',
        'FeedIndex': '媒体指数',
        'NewsIndex': '新闻指数'
    }
    # 创建Tag对象表明要抓取的指数类型
    tag = Tag('SearchIndex')
    # 设定几个需要获取指数的url并逐个进行数据爬取，最后再进行封装存储成excel文件
    with open('area_data/provinces_code.json', 'r', encoding='utf-8') as f_provinces:
        provinces = json.load(f_provinces)
    with open('area_data/citys_code.json', 'r', encoding='utf-8') as f_cities:
        cities = json.load(f_cities)
    # 获取cookie
    with open('cookies', 'r') as f:
        cookies = []
        for i in f:
            cookies.append(i.replace('\n', ''))
    # 应该创建所需要的路径目录
    if not os.path.exists(target_path):
        # 创建主目录
        if target_path != '.':
            os.mkdir(target_path)
        sub_dir = target_dirs[target]
        os.mkdir(target_path + '/{}/'.format(sub_dir))
    # 构造一个主集合
    target_data = dict()
    print('正在获取全国数据...')
    target_data['National'] = getNationalData(cookies[0],keyword, startDate, endDate, tag)
    print('正在获取省份数据...')
    target_data['Province'] = getProvinceData(cookies[0], keyword, startDate, endDate, provinces, tag)
    print('正在获取市级数据...')
    target_data['City'] = getCitysData(cookies[0], keyword, startDate, endDate, cities, tag)
    with open('temp/tempdata.json', 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(target_data))
    print('开始导出数据...')
    pack = datapack.Pack(target_data, target_path, keyword, tag._target)
    # 将数据导出成excel文件
    # with open('/Users/wangyao/Desktop/temp_data/test_data.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(target_data['Province']))
    print('Done!')


if __name__ == '__main__':
    start_time = time.time()
    # main('上市', '2019-06-30', '2019-08-01', '/Users/wangyao/Desktop/result')

    end_time = time.time() - start_time
    print('耗时 {} s'.format(end_time))
