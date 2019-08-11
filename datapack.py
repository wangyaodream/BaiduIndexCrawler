import xlwt
import datetime

NAME_MAP = {'SearchIndex': '搜索指数', 'FeedIndex': '资讯指数', 'NewsIndex': '媒体指数'}

class Pack:
    def __init__(self, tag_data, tag_path, keyword, target):
        """
        初始化pack对象，直接将数据导出成excel
        :param tag_data: 目标数据
        :param tag_path: 存储源路径
        :param keyword: 关键字
        """
        self._tag_data = tag_data
        self._tag_path = tag_path
        self._keyword = keyword  # keyword用来制作表头的字符串
        self._target = target
        self.fmt_data()  # 运行存储


    def fmt_data(self):
        # 存储搜索指数
        if self._target not in 'SearchIndex FeedIndex NewsIndex'.split():
            raise Exception('Unreasonably target')
        if self._target == 'SearchIndex':
            self.searchIndexProcess()
        elif self._target == 'FeedIndex':
            # 存储咨询指数
            self.feedIndexProcess()
        else:
            # 存储媒体指数
            self.newsIndexProcess()

    def searchIndexProcess(self):
        """这个代表searchIndex指数的所有数据，所以应该是它来创建excel对象并储存
            在使用的self._tag_data 是一个整体数据的集合，使用的时候要注意
        """
        workbook = xlwt.Workbook(encoding='utf-8')
        filename = '{}_{}_搜索指数.xls'.format(datetime.datetime.now().strftime('%y%m%d%m%S'), self._keyword)
        national_titles = '日期 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword).split()
        self.national_sheet(workbook, national_titles, self._tag_data['National'])
        province_titles = '日期 省份 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword, self._keyword).split()
        self.provinces_sheet(workbook, province_titles, self._tag_data['Province'])
        city_titles = '日期 城市名 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword, self._keyword).split()
        self.citys_sheet(workbook, city_titles, self._tag_data['City'])
        # save file

        file_path = '{}/{}/{}'.format(self._tag_path, '搜索指数', filename)
        workbook.save(file_path)

    def feedIndexProcess(self):
        """资讯指数数据存储成excel"""
        workbook = xlwt.Workbook(encoding='utf-8')
        filename = '{}_{}_资讯指数.xls'.format(datetime.datetime.now().strftime('%y%m%d%m%S'), self._keyword)
        # 资讯指数也分全国、省份、市级,但是不区分移动或pc
        national_titles = '日期 {}_资讯_指数'.format(self._keyword).split()
        self.national_sheet(workbook, national_titles, self._tag_data['National'], False)
        province_titles = '日期 省份 {}_资讯_指数'.format(self._keyword).split()
        self.provinces_sheet(workbook, province_titles, self._tag_data['Province'], False)
        city_titles = '日期 城市名 {}_资讯_指数'.format(self._keyword).split()
        self.citys_sheet(workbook, city_titles, self._tag_data['City'], False)
        # save file
        file_path = '{}/{}/{}'.format(self._tag_path, '资讯指数', filename)
        workbook.save(file_path)

    def newsIndexProcess(self):
        """媒体指数"""
        workbook = xlwt.Workbook(encoding='utf-8')
        filename = '{}_{}_媒体指数.xls'.format(datetime.datetime.now().strftime('%y%m%d%m%S'), self._keyword)
        # 资讯指数也分全国、省份、市级,但是不区分移动或pc
        national_titles = '日期 {}_媒体_指数'.format(self._keyword).split()
        self.national_sheet(workbook, national_titles, self._tag_data['National'], False)
        province_titles = '日期 省份 {}_媒体_指数'.format(self._keyword).split()
        self.provinces_sheet(workbook, province_titles, self._tag_data['Province'], False)
        city_titles = '日期 城市名 {}_媒体_指数'.format(self._keyword).split()
        self.citys_sheet(workbook, city_titles, self._tag_data['City'], False)
        # save file
        file_path = '{}/{}/{}'.format(self._tag_path, '媒体指数', filename)
        workbook.save(file_path)

    @staticmethod
    def init_sheet(_worksheet, title):
        for i in range(len(title)):
            _worksheet.write(0, i, title[i])

    @staticmethod
    def national_sheet(workbook: xlwt.Workbook, titles: list, tag_data, specific=True):
        worksheet = workbook.add_sheet('全国')
        # 初始化构造title
        Pack.init_sheet(worksheet, titles)
        # 填充内容
        fill_row = 1
        for _ in tag_data['all']:
            if specific:
                temp_data = [
                    tag_data['all'][fill_row - 1]['date'],
                    tag_data['all'][fill_row - 1]['index'],
                    tag_data['pc'][fill_row - 1]['index'],
                    tag_data['wise'][fill_row - 1]['index'],
                ]
            else:
                temp_data = [
                    tag_data['all'][fill_row - 1]['date'],
                    tag_data['all'][fill_row - 1]['index'],
                ]
            for j in range(len(temp_data)):
                worksheet.write(fill_row, j, temp_data[j])
            fill_row += 1

    @staticmethod
    def provinces_sheet(workbook: xlwt.Workbook, titles, tag_data, specific=True):
        worksheet = workbook.add_sheet('省份')
        # init title
        Pack.init_sheet(worksheet, titles)
        # fill data
        fill_row = 1
        for tag in tag_data:
            cursor_index = 0
            for _ in tag_data[tag]['all']:
                if specific:
                    temp_data = [
                        tag_data[tag]['all'][cursor_index]['date'],
                        tag,
                        tag_data[tag]['all'][cursor_index]['index'],
                        tag_data[tag]['pc'][cursor_index]['index'],
                        tag_data[tag]['wise'][cursor_index]['index'],
                    ]
                else:
                    temp_data = [
                        tag_data[tag]['all'][cursor_index]['date'],
                        tag,
                        tag_data[tag]['all'][cursor_index]['index'],
                    ]
                for j in range(len(temp_data)):
                    worksheet.write(fill_row, j, temp_data[j])
                fill_row += 1
                cursor_index += 1

    @staticmethod
    def citys_sheet(workbook: xlwt.Workbook, titles, tag_data, specific=True):
        # 根据条目进行分栏
        total_row = data_count(tag_data)
        sheet_count = 0
        sheets = []
        for i in range(total_row):
            if i % 65534 == 0:
                _worksheet = workbook.add_sheet('市级_%d' % sheet_count)
                Pack.init_sheet(_worksheet, titles)
                sheets.append(_worksheet)
                sheet_count += 1

        # worksheet = workbook.add_sheet('市级')
        # init title
        sheet_index = 0
        # fill data
        fill_row = 1
        index_count = 1
        for tag in tag_data:
            cursor_index = 0
            for _ in tag_data[tag]['all']:
                if specific:
                    temp_data = [
                        tag_data[tag]['all'][cursor_index]['date'],
                        tag,
                        tag_data[tag]['all'][cursor_index]['index'],
                        tag_data[tag]['pc'][cursor_index]['index'],
                        tag_data[tag]['wise'][cursor_index]['index'],
                    ]
                else:
                    temp_data = [
                        tag_data[tag]['all'][cursor_index]['date'],
                        tag,
                        tag_data[tag]['all'][cursor_index]['index'],
                    ]
                # 判断是哪一个sheet
                if index_count % 65534 == 0:
                    sheet_index += 1
                    fill_row = 1

                for j in range(len(temp_data)):
                    try:
                        sheets[sheet_index].write(fill_row, j, temp_data[j])
                    except IndexError:
                        print('sheets len:{} , sheet_index: {}, fill_row: {}, index_count: {}'.format(len(sheets), sheet_index, fill_row, index_count))
                fill_row += 1
                index_count += 1
                cursor_index += 1


def data_count(data):
    _count = 0
    for i in data:
        _count += len(data[i]['all'])
    return _count


if __name__ == '__main__':
    import json
    print('Start...')
    with open('temp/tempdata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    workbook = xlwt.Workbook(encoding='utf-8')
    titles = 'date county index'.split()
    Pack.citys_sheet(workbook, titles, data['City'], False)
    print('Saving...')
    workbook.save('E:/tmp_data/info.xls')
    print('OK!')




