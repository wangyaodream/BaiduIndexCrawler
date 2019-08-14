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

with open('temp/access_info.json', 'r') as acc_f:
    access_dict = json.load(acc_f)
access_count = access_dict['access_count']

headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttoRequest',
    'User-Agent': (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    )

}


class StatusException(Exception):
    def __init__(self, e):
        super().__init__(self)
        message = {
            10001: '该账号访问受限，明天再试',
            10002: '无该关键词'
        }
        self._msg = message[e]
        # 将访问计数记录
        global access_count
        global access_dict
        access_dict['access_count'] = access_count
        with open('temp/access_info.json', 'w') as acc_w:
            acc_w.write(json.dumps(access_dict))

    def __str__(self):
        return self._msg


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
    def __init__(self, cookie, target, keywords, start_date, end_date, area=0):
        """
        初始化BaiduIndex对象，赋予一些基本属性
        :param keywords: 关键词
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param area: 区域，默认0代表全国（地区代码需要自己总结）
        """
        self._cookie = cookie
        self._target = target
        self._keywords = keywords
        self._time_range_list = self.get_time_range_list(start_date, end_date)
        self._all_kind = ['all', 'pc', 'wise']
        self._area = area
        self.result = {keyword: defaultdict(list) for keyword in [self._keywords]}
        self.get_result()

    def get_result(self):
        for start_date, end_date in self._time_range_list:
            encrypt_datas, uniqid = self.get_encrypt_datas(start_date, end_date)
            key = self.get_key(uniqid)
            if 'all' in encrypt_datas[0]:
                for encrypt_data in encrypt_datas:
                    for kind in self._all_kind:
                        encrypt_data[kind]['data'] = self.decrypt_func(key, encrypt_data[kind]['data'])
                    self.format_data(encrypt_data)
            else:
                for encrypt_data_2 in encrypt_datas:
                    encrypt_data_2['data'] = self.decrypt_func(key, encrypt_data_2['data'])
                self.format_data(encrypt_data_2, False)

    def get_encrypt_datas(self, start_date, end_date):
        """
        获取加密的数据
        :param start_date: 格式化后的开始日期
        :param end_date: 格式化后的结束日期
        :param tag_url: 需要访问的目标url
        :return: 加密的结果数据
        """
        request_args = {
            'word': self._keywords,
            'startDate': start_date,
            'endDate': end_date,
            'area': self._area,
        }
        # 通过指定目标构造url
        tag = Tag(self._target)
        url = tag.structure_urls(request_args)
        # 获取页面数据
        html = self.http_get(url, self._cookie)
        datas = json.loads(html)
        if datas['status'] != 0:
            raise StatusException(datas['status'])
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


def getNationalData(cookie, keyword, startDate, endDate, target):
    # 获取全国的数据
    global access_count
    access_count += 1
    bi = BaiduIndex(cookie, target, keyword, startDate, endDate, 0)
    result_data = dict(bi.result[keyword])
    return result_data


def getProvinceData(cookie, keyword, startDate, endDate, provinceMap, target):
    result_data = {}
    thread_list = []
    for curr_province in provinceMap:
        # time.sleep(0.1)
        province_code = provinceMap[curr_province]
        # 单线程
        global access_count
        access_count += 1
        bi = BaiduIndex(cookie, target, keyword, startDate, endDate, province_code)
        temp_data = dict(bi.result[keyword])
        result_data[curr_province] = temp_data

        # 多线程
    #     t = MyThread(BaiduIndex, args=(cookie, target, keyword, startDate, endDate, province_code))
    #     thread_list.append((curr_province, t))
    #     t.start()
    # for province, t in thread_list:
    #     t.join()
    #     res = t.get_result()
    #     result_data[province] = dict(res.result[keyword])

    return result_data


def getCitysData(cookie, keyword, startDate, endDate, citysMap, target):
    result_data = {}
    citys_data = {}
    thread_list = []
    for i in citysMap:
        citys_data.update(citysMap[i])
    for city in citys_data:

        city_code = citys_data[city]
        # 单线程
        global access_count
        access_count += 1
        bi = BaiduIndex(cookie, target, keyword, startDate, endDate, city_code)
        temp_data = dict(bi.result[keyword])
        result_data[city] = temp_data
        # 多线程
    #     t = MyThread(BaiduIndex, args=(cookie, target, keyword, startDate, endDate, city_code))
    #     thread_list.append((city, t))
    #     t.start()
    # for city, t in thread_list:
    #     t.join()
    #     res = t.get_result()
    #     result_data[city] = dict(res.result[keyword])
    return result_data


def main(keyword, startDate, endDate, target, main_path='.'):
    target_dirs = {
        'SearchIndex': '搜索指数',
        'FeedIndex': '资讯指数',
        'NewsIndex': '媒体指数'
    }
    sub_dir = "{}/{}".format(main_path, target_dirs[target])
    # 创建Tag对象表明要抓取的指数类型
    # 设定几个需要获取指数的url并逐个进行数据爬取，最后再进行封装存储成excel文件
    with open('area_data/provinces_code.json', 'r', encoding='utf-8') as f_provinces:
        provinces = json.load(f_provinces)
    with open('area_data/cities_code_bak.json', 'r', encoding='utf-8') as f_cities:
        cities = json.load(f_cities)

    # 获取cookie
    with open('cookies', 'r') as f:
        cookies = []
        for i in f:
            cookies.append(i.replace('\n', ''))

    # 应该创建所需要的路径目录
    if not os.path.exists(main_path):
        # 创建主目录
        if main_path != '.':
            os.mkdir(main_path)
        os.mkdir(sub_dir)
    else:
        # 有主目录没有sub目录
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
    # 构造一个主集合
    target_data = {}
    print('正在获取全国数据...')
    target_data['National'] = getNationalData(cookies[0], keyword, startDate, endDate, target)
    print('正在获取省份数据...')
    target_data['Province'] = getProvinceData(cookies[0], keyword, startDate, endDate, provinces, target)
    print('正在获取市级数据...')
    target_data['City'] = getCitysData(cookies[0], keyword, startDate, endDate, cities, target)

    # 清空缓存
    if os.path.exists('temp/tempdata.json'):
        os.remove('temp/tempdata.json')
    # 写入缓存文件
    with open('temp/tempdata.json', 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(target_data))
    print('开始导出数据...')

    pack = datapack.Pack(target_data, main_path, keyword, target)
    # 将数据导出成excel文件
    # with open('/Users/wangyao/Desktop/temp_data/test_data.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(target_data['Province']))

    # 将访问计数记录
    global access_count
    global access_dict
    access_dict['access_count'] = access_count
    with open('temp/access_info.json', 'w') as acc_w:
        acc_w.write(json.dumps(access_dict))
    print('Done!')


if __name__ == '__main__':
    # target_map = {
    #     "搜索指数": 'SearchIndex',
    #     "资讯指数": "FeedIndex",
    #     "媒体指数": "NewsIndex"
    # }
    # # cmd UI
    # # keyword = input("请输入关键词: ")
    # # start_date = input("请输入开始时间(XXXX-XX-XX): ")
    # # end_date = input("请输入结束时间(XXXX-XX-XX): ")
    # # target = target_map[input("请输入指数类型（搜索指数，资讯指数，媒体指数）: ")]
    # # tag_path = input('请输入数据存储路径: ')
    #
    ##############################################################################
    start_time = time.time()
    # # path for mac
    # main_path = '/Users/wangyao/Desktop/result'
    #
    # # path for windows
    main_path = 'E:/tmp_data/result'
    # main(keyword, start_date, end_date, target, tag_path)
    try:
        main('python', '2013-01-01', '2014-01-01', 'SearchIndex', main_path)
    except StatusException as e:
        print(e)
    #
    end_time = time.time() - start_time
    print('耗时 {} s'.format(end_time))

    #################################################################################
    # # 原始数据测试
    # key = 'or1D,h%giuK2jWI7-.69%2,+813504'
    # data = 'u2uoogojD%WgDIK2DgjuDo,gDDDoDgD2,%DgoWuKWgooDW2gjo2uWgoK%jogD%,2ogD22DIgDjKougj,IuWgjuKDIgjoWoogIu2,jgIDWu2gD2jjIgj,%,KgDDW%ugjuu%DgjjW2%gID2%KgIj,oDgjoIWjgD2Do,gDj,j2gDo,IjgDDDW2gjouj,gj2IKWgDjWoKgDoWo,gD%,KugD%IjugDWWKugj2WDogjW,uKgjuuoogj,uIWgDWD2Wgj,WujgjoDujgI,Kj,gIouo,gIjoKIgDWIo,gDW2j2gj,oW%gjoD%2gjIjI%gIDuIDgI%u2IgI22%KgI2uoWgIIK2DgIjD2ugII,DugIj%KugjDIuogjD%,2gjjoI%gjIIDjgj%j2WgIu%,2gIDI,%gj2j2KgjIDKjgjDKo2gjIo,Igj%I2KgID,,jgIDKWogj2%,ugjjWuDgjjKj,gj2ou,gj%%oogIDK2IgI2jIWgjWIj%gjKKj2gjWKIDgjK,uWgj%oDWgIDuIogIj%,ugj%juKgj2%WugjIWjDgjK,jjgjW%IjgIIIDDgI%W,Wgj2Ijjgj2u%DgjIIIDgj2Wo%gj%DWogIujjWgIu%jugj2IoogjI,uugjjI,ugj2u,%gj%%22gIu,IogIDjDIgj%ouugj2j2,gj2jo2gj2oWogj22,DgjWDIDgjW%KWgjIDDKgjoK%DgjjI2IgjooK%gj%juugIoKDDgIDWjDgj%IjKgjIDjugD,WougD2,D%gjD%%%gI,jDKgIou2ogojjW,gjujuKgjuWWKgjDK2Dgj2IWDgI,oDIgID2oKgIuuKWgjWoK,gjKoDjgjKIuKgIu,IWgIuWjugIj%oWgIWooog2,o2ogI,Ij2gjKj2Igj2%o2gI,,2%gIDDoWgjK2K,gjKj%DgjK,2WgjW,KjgjWKjDgIDo%DgIIou%gI,jIDgI,K2,gI,KuDgI,W,ogI,jW,gIo%oIgIj%uIgIuuDKgI,,oKgDK,uogDj%uDgj,%2jgj2%jWgI,uKogj%,WIgj%%W,gj%%IIgjWK,KgID%ougI%j%Dg2,,W2g2Wu%%g2WuDugIW,2,gIIKIKgID%,ogIoK,DgIojougj%%KogjuWu%gju2%%gjojDKgjooK,gjKo2DgIuoDKgjDoIIgjo%%Dgj2WK,gjDWK%gjjK,%gj2KIogj2W%jgDKjjKgDWoj,gDW%KWgj,,K%gjujuIgjjjjIgjWuDjgjooj2gj,K,Dgj,2,KgjD2uIgjI2KKgj%%,ogj%Io%gjoWW2gjoW,2gjujI%gj,W%Wgj,ouIgjIIIIgjWoDDgju2j%gjoo22gj,IuKgDK,22gDWIj%gjIWWugjWIDDgjoIIDgjujjDgj,%K,gD%KD2gjo%2Igj%IoDgIuuIKgjjWoogjD2%%gjj,,ugjIIDDgIoj%WgIDu%KgIDI%KgjI,DIgjojuugDWWKogjooojgjoKoWgj%jDogI,,o,gjD,2ugjjI2%gjj,%Dgjuj,ogjD2KWgj%,2WgjWIougjDDI2gj2uK%gj2KuWgj2IIugDoj%WgDK,,2gDKj%ogjuojWgjID2%gIuWjKgIuuDIgIouIIgIDuoKgj2oW%gjuuo,gjDI%2gjuuu,gDWjj,gj,K,Wgjj2,ogj%KIIgj,o%jgD2oj%gDWIKIgj,j%ogjou%Wgjj2%Wgj2u%uguI2WDgo2D,2goKWuKgDojujgDjuKogD%ID2gj,IDjgD%,IDgD%Wj,gDjI%jgoW22IgD%juKgDWDuogDW2u%guojI2g,2uu,go2KDWgDo%u2gjII2ogj2I%,gjjuIKgoWWojgDuI%ogoKojDgo%oKogDIoj2gjjuIjgj%%I,gDW2%IgjuIIogj,,%ogj,uIKgju22WgjKWIogIu2I%gjooW2gjD,2KgjuoWIgjojWogjDD2ugj%jo%gIu,j2gjou%%gDWIj,gDW2D%gDWuI%gjojKogjWI,DgI,IK%gju22ugjoDKugjo2uIgjDWIWgjIujIgI,2o2gIoDW%gj,ojugj,2,%gju%,jgjojj,gjDKj,gI,2IWgIu,IogDID%DgDj,%jgDj,o%gDKj2ugjoj,KgjjWoKgjKoD2gDW2I2gj,%2ugDKK%ugDWj%%gjujo,gjWu2ugI,uo%gjDj,ogjI%jugjDuKjgjo%j%gjDKu%'
    # res = BaiduIndex.decrypt_func(key, data)
    # print(res)
    # print(len(res))

    # 结果数据测试
    # tag = Tag('NewsIndex')
    # with open('temp/tempdata.json', 'r', encoding='utf-8') as f:
    #     tag_data = json.load(f)
    # pack = datapack.Pack(tag_data, main_path, '福特', tag._target)

    # 时间轴测试
    # tmp = BaiduIndex.get_time_range_list('2016-01-01', '2019-01-01')
    # print(len(tmp))
    # print(tmp)