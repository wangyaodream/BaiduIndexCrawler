from urllib.parse import urlencode
from collections import defaultdict
import datetime
import requests
import json
# import pandas as pd
# import numpy as np
# from sfi import Data

# 登录之后，百度首页的请求cookies，必填
COOKIES = 'BAIDUID=5A31D2B14DDE35A11B48BDC77CF6C99D:FG=1; BIDUPSID=5A31D2B14DDE35A11B48BDC77CF6C99D; PSTM=1564373659; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1564402025,1564466842,1565009840; H_PS_PSSID=1439_21114_29522_29518_29098_29568_28834_29221_26350_29461; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=1; delPer=0; BDUSS=ZMVGh2azR2NkhxRGFUU0o1YXNaZG5Xen56YTAyQy1RLTFHQVJ0Z0lDRldNWE5kSVFBQUFBJCQAAAAAAAAAAAEAAABB1EVCs8HP48Lk17kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFakS11WpEtdQm; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1565238361; bdindexid=9m4euo4pr6803oe71jd34c9d93'
headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


class BaiduIndex:
    """
        百度搜索指数
        :keywords; list or string '<keyword>,<keyword>'
        :start_date; string '2018-10-02'
        :end_date; string '2018-10-02'
        :area; int, search by cls.province_code/cls.city_code
    """


    def __init__(self, keywords, start_date, end_date, area=0):
        self._keywords = keywords if isinstance(keywords, list) else keywords.split(',')
        self._time_range_list = self.get_time_range_list(start_date, end_date)
        self._all_kind = ['all', 'pc', 'wise']
        self._area = area
        self.result = {keyword: defaultdict(list) for keyword in self._keywords}
        self.get_result()

    def get_result(self):
        for start_date, end_date in self._time_range_list:
            encrypt_datas, uniqid = self.get_encrypt_datas(start_date, end_date)
            key = self.get_key(uniqid)
            for encrypt_data in encrypt_datas:
                for kind in self._all_kind:
                    encrypt_data[kind]['data'] = self.decrypt_func(key, encrypt_data[kind]['data'])
                self.format_data(encrypt_data)

    def get_encrypt_datas(self, start_date, end_date):
        request_args = {
            'word': ','.join(self._keywords),
            'startDate': start_date,
            'endDate': end_date,
            'area': self._area,
        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        html = self.http_get(url)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def get_key(self, uniqid):
        url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self.http_get(url)
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
    def http_get(url, cookies=COOKIES):
        headers['Cookie'] = cookies
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @staticmethod
    def get_time_range_list(startdate, enddate):
        """
        max 6 months
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            tempdate = startdate + datetime.timedelta(days=300)
            if tempdate > enddate:
                all_days = (enddate-startdate).days
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
        for o in range(len(a)//2):
            n[a[o]] = a[len(a)//2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')


if __name__ == '__main__':
    baidu_index = BaiduIndex(keywords=['股票'], start_date='2018-01-01', end_date='2019-07-06')
    bz = baidu_index.result['股票']
    # df=pd.DataFrame(bz['all'])
    # count_row=df.shape[0]
    # for i in range(count_row,10000):
    #     df.loc[i]='NA'
    # # Data.addVarStrL('time')
    # # Data.addVarStrL('search')
    # # Data.store('time',None,df["date"])
    # # Data.store('search',None,df["index"])