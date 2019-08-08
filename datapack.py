import xlwt
import datetime
import json

NAME_MAP = {'SearchIndex': '搜索指数', 'FeedIndex': '资讯指数', 'NewsIndex': '媒体指数'}

class Pack:
    def __init__(self, tag_data, tag_path, keyword):
        """
        初始化pack对象，直接将数据导出成excel
        :param tag_data: 目标数据
        :param tag_path: 存储源路径
        :param keyword: 关键字
        """
        self._tag_data = tag_data
        self._tag_path = tag_path
        self._keyword = keyword  # keyword用来制作表头的字符串
        self.fmt_data()  # 运行存储


    def fmt_data(self):
        # 存储搜索指数
        self.searchIndexProcess()
        # 存储咨询指数
        self.feedIndexProcess()
        # 存储媒体指数
        self.newsIndexProcess()
        

    def searchIndexProcess(self):
        """这个代表searchIndex指数的所有数据，所以应该是它来创建excel对象并储存
            在使用的self._tag_data 是一个整体数据的集合，使用的时候要注意
        """
        workbook = xlwt.Workbook(encoding='utf-8')
        filename = '{}_搜索指数.xls'.format(datetime.datetime.now().strftime('%y%m%d%m%S'))
        national_titles = '日期 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword).split()
        self.national_sheet(workbook, national_titles, self._tag_data['National'], 'SearchIndex')
        province_titles = '日期 省份 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword, self._keyword).split()
        self.provinces_sheet(workbook, province_titles, self._tag_data['Province'], 'SearchIndex')
        city_titles = '日期 城市名 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword, self._keyword).split()
        self.citys_sheet(workbook, city_titles, self._tag_data['City'], 'SearchIndex')
        # save file

        file_path = '{}/{}/{}'.format(self._tag_path, '搜索指数', filename)
        workbook.save(file_path)

    def feedIndexProcess(self):
        """资讯指数数据存储成excel"""
        workbook = xlwt.Workbook(encoding='utf-8')
        filename = '{}_资讯指数.xls'.format(datetime.datetime.now().strftime('%y%m%d%m%S'))
        # 资讯指数也分全国、省份、市级,但是不区分移动或pc
        national_titles = '日期 {}_资讯_指数'.format(self._keyword).split()
        self.national_sheet(workbook, national_titles, self._tag_data['National'], 'FeedIndex', False)
        province_titles = '日期 省份 {}_资讯_指数'.format(self._keyword).split()
        self.provinces_sheet(workbook, province_titles, self._tag_data['Province'], 'FeedIndex', False)
        city_titles = '日期 城市名 {}_资讯_指数'.format(self._keyword).split()
        self.citys_sheet(workbook, city_titles, self._tag_data['City'], 'FeedIndex', False)
        # save file
        file_path = '{}/{}/{}'.format(self._tag_path, '资讯指数', filename)
        workbook.save(file_path)

    def newsIndexProcess(self):
        """媒体指数"""
        workbook = xlwt.Workbook(encoding='utf-8')
        filename = '{}_{}_媒体指数.xls'.format(datetime.datetime.now().strftime('%y%m%d%m%S'), self._keyword)
        # 资讯指数也分全国、省份、市级,但是不区分移动或pc
        national_titles = '日期 {}_媒体_指数'.format(self._keyword).split()
        self.national_sheet(workbook, national_titles, self._tag_data['National'], 'NewsIndex', False)
        province_titles = '日期 省份 {}_媒体_指数'.format(self._keyword).split()
        self.provinces_sheet(workbook, province_titles, self._tag_data['Province'], 'NewsIndex', False)
        city_titles = '日期 城市名 {}_媒体_指数'.format(self._keyword).split()
        self.citys_sheet(workbook, city_titles, self._tag_data['City'], 'NewsIndex', False)
        # save file
        file_path = '{}/{}/{}'.format(self._tag_path, '媒体指数', filename)
        workbook.save(file_path)

    @staticmethod
    def init_sheet(_worksheet, title):
        for i in range(len(title)):
            _worksheet.write(0, i, title[i])

    @staticmethod
    def national_sheet(workbook: xlwt.Workbook, titles: list, tag_data, item_name, specific=True):
        worksheet = workbook.add_sheet('全国')
        # 初始化构造title
        Pack.init_sheet(worksheet, titles)
        #填充内容
        fill_row = 1
        for _ in tag_data[item_name]['all']:
            if specific:
                temp_data = [
                    tag_data[item_name]['all'][fill_row - 1]['date'],
                    tag_data[item_name]['all'][fill_row - 1]['index'],
                    tag_data[item_name]['pc'][fill_row - 1]['index'],
                    tag_data[item_name]['wise'][fill_row - 1]['index'],
                ]
            else:
                temp_data = [
                    tag_data[item_name]['all'][fill_row - 1]['date'],
                    tag_data[item_name]['all'][fill_row - 1]['index'],
                ]
            for j in range(len(temp_data)):
                worksheet.write(fill_row, j, temp_data[j])
            fill_row += 1

    @staticmethod
    def provinces_sheet(workbook: xlwt.Workbook, titles, tag_data, item_name, specific=True):
        worksheet = workbook.add_sheet('省份')
        # init title
        Pack.init_sheet(worksheet, titles)
        # fill data
        fill_row = 1
        for tag in tag_data:
            cursor_index = 0
            for _ in tag_data[tag][item_name]['all']:
                if specific:
                    temp_data = [
                        tag_data[tag][item_name]['all'][cursor_index]['date'],
                        tag,
                        tag_data[tag][item_name]['all'][cursor_index]['index'],
                        tag_data[tag][item_name]['pc'][cursor_index]['index'],
                        tag_data[tag][item_name]['wise'][cursor_index]['index'],
                    ]
                else:
                    temp_data = [
                        tag_data[tag][item_name]['all'][cursor_index]['date'],
                        tag,
                        tag_data[tag][item_name]['all'][cursor_index]['index'],
                    ]
                for j in range(len(temp_data)):
                    worksheet.write(fill_row, j, temp_data[j])
                fill_row += 1
                cursor_index += 1

    @staticmethod
    def citys_sheet(workbook: xlwt.Workbook, titles, tag_data, item_name, specific=True):
        worksheet = workbook.add_sheet('市级')
        # init title
        Pack.init_sheet(worksheet, titles)
        # fill data
        fill_row = 1
        for tag in tag_data:
            cursor_index = 0
            for _ in tag_data[tag][item_name]['all']:
                if specific:
                    temp_data = [
                        tag_data[tag][item_name]['all'][cursor_index]['date'],
                        tag,
                        tag_data[tag][item_name]['all'][cursor_index]['index'],
                        tag_data[tag][item_name]['pc'][cursor_index]['index'],
                        tag_data[tag][item_name]['wise'][cursor_index]['index'],
                    ]
                else:
                    temp_data = [
                        tag_data[tag][item_name]['all'][cursor_index]['date'],
                        tag,
                        tag_data[tag][item_name]['all'][cursor_index]['index'],
                    ]
                for j in range(len(temp_data)):
                    worksheet.write(fill_row, j, temp_data[j])
                fill_row += 1
                cursor_index += 1










