import xlwt
import datetime
import uuid

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
        self._tag_path = tag_path if tag_path[-1] != '/' else tag_path[:-1]
        self._keyword = keyword  # keyword用来制作表头的字符串
        self._target = target
        self._tag_id = uuid.uuid1().__str__()[-12:]
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
        # workbook = xlwt.Workbook(encoding='utf-8')
        sub_path = '{}/{}'.format(self._tag_path, '搜索指数')
        national_titles = '日期 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword).split()
        self.national_sheet(national_titles, self._tag_data['National'], sub_path, self._tag_id, self._keyword)
        province_titles = '日期 省份 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword, self._keyword).split()
        self.provinces_sheet(province_titles, self._tag_data['Province'], sub_path, self._tag_id, self._keyword)
        city_titles = '日期 城市名 {}_整体 {}_PC {}_移动'.format(self._keyword, self._keyword, self._keyword, self._keyword).split()
        self.citys_sheet(city_titles, self._tag_data['City'], sub_path, self._tag_id, self._keyword)

    def feedIndexProcess(self):
        """资讯指数数据存储成excel"""
        # workbook = xlwt.Workbook(encoding='utf-8')
        sub_path = '{}/{}'.format(self._tag_path, '资讯指数')
        # 资讯指数也分全国、省份、市级,但是不区分移动或pc
        national_titles = '日期 {}_资讯_指数'.format(self._keyword).split()
        self.national_sheet(national_titles, self._tag_data['National'], sub_path, self._tag_id, self._keyword, False)
        province_titles = '日期 省份 {}_资讯_指数'.format(self._keyword).split()
        self.provinces_sheet(province_titles, self._tag_data['Province'], sub_path, self._tag_id, self._keyword, False)
        city_titles = '日期 城市名 {}_资讯_指数'.format(self._keyword).split()
        self.citys_sheet(city_titles, self._tag_data['City'], sub_path, self._tag_id, self._keyword, False)

    def newsIndexProcess(self):
        """媒体指数"""
        # workbook = xlwt.Workbook(encoding='utf-8')
        sub_path = '{}/{}'.format(self._tag_path, '媒体指数')
        # 资讯指数也分全国、省份、市级,但是不区分移动或pc
        national_titles = '日期 {}_媒体_指数'.format(self._keyword).split()
        self.national_sheet(national_titles, self._tag_data['National'], sub_path, self._tag_id, self._keyword, False)
        province_titles = '日期 省份 {}_媒体_指数'.format(self._keyword).split()
        self.provinces_sheet(province_titles, self._tag_data['Province'], sub_path, self._tag_id, self._keyword, False)
        city_titles = '日期 城市名 {}_媒体_指数'.format(self._keyword).split()
        self.citys_sheet(city_titles, self._tag_data['City'], sub_path, self._tag_id, self._keyword, False)

    @staticmethod
    def init_sheet(_worksheet, title):
        for i in range(len(title)):
            _worksheet.write(0, i, title[i])

    @staticmethod
    def national_sheet(titles: list, tag_data, tag_path, tag_id, keyword, specific=True):
        workbook = xlwt.Workbook(encoding='utf-8')
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
        # save file
        workbook.save('{}/{}_{}_{}.xls'.format(tag_path, tag_id, keyword, '全国'))

    @staticmethod
    def provinces_sheet(titles, tag_data, tag_path, tag_id, keyword, specific=True):
        # 根据条目进行分栏
        total_row = data_count(tag_data)
        sheets = []
        workbooks = []
        for i in range(total_row):
            if i % 65534 == 0:
                _workbook = xlwt.Workbook(encoding='utf-8')
                _sheet = _workbook.add_sheet('省级')
                Pack.init_sheet(_sheet, titles)
                sheets.append(_sheet)
                workbooks.append(_workbook)
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
                        print('sheets len:{} , sheet_index: {}, fill_row: {}, index_count: {}'.format(len(sheets),
                                                                                                      sheet_index,
                                                                                                      fill_row,
                                                                                                      index_count))
                fill_row += 1
                index_count += 1
                cursor_index += 1
        workbook_index = 1
        for workbook in workbooks:
            workbook.save('{}/{}_{}_省级_{}.xls'.format(tag_path, tag_id, keyword, workbook_index))
            workbook_index += 1

    # ############original###########
    # @staticmethod
    # def citys_sheet(workbook: xlwt.Workbook, titles, tag_data, specific=True):
    #     # 根据条目进行分栏
    #     total_row = data_count(tag_data)
    #     sheet_count = 0
    #     sheets = []
    #     for i in range(total_row):
    #         if i % 65534 == 0:
    #             _worksheet = workbook.add_sheet('市级_%d' % sheet_count)
    #             Pack.init_sheet(_worksheet, titles)
    #             sheets.append(_worksheet)
    #             sheet_count += 1
    #
    #     # worksheet = workbook.add_sheet('市级')
    #     # init title
    #     sheet_index = 0
    #     # fill data
    #     fill_row = 1
    #     index_count = 1
    #     for tag in tag_data:
    #         cursor_index = 0
    #         for _ in tag_data[tag]['all']:
    #             if specific:
    #                 temp_data = [
    #                     tag_data[tag]['all'][cursor_index]['date'],
    #                     tag,
    #                     tag_data[tag]['all'][cursor_index]['index'],
    #                     tag_data[tag]['pc'][cursor_index]['index'],
    #                     tag_data[tag]['wise'][cursor_index]['index'],
    #                 ]
    #             else:
    #                 temp_data = [
    #                     tag_data[tag]['all'][cursor_index]['date'],
    #                     tag,
    #                     tag_data[tag]['all'][cursor_index]['index'],
    #                 ]
    #             # 判断是哪一个sheet
    #             if index_count % 65534 == 0:
    #                 sheet_index += 1
    #                 fill_row = 1
    #
    #             for j in range(len(temp_data)):
    #                 try:
    #                     sheets[sheet_index].write(fill_row, j, temp_data[j])
    #                 except IndexError:
    #                     print('sheets len:{} ,
    #                     sheet_index: {},
    #                     fill_row: {},
    #                     index_count: {}'.format(len(sheets), sheet_index, fill_row, index_count))
    #             fill_row += 1
    #             index_count += 1
    #             cursor_index += 1
    @staticmethod
    def citys_sheet(titles, tag_data, tag_path, tag_id, keyword, specific=True):

        # 根据条目进行分栏
        total_row = data_count(tag_data)
        sheets = []
        workbooks = []
        for i in range(total_row):
            if i % 65534 == 0:
                _workbook = xlwt.Workbook(encoding='utf-8')
                _sheet = _workbook.add_sheet('市级')
                Pack.init_sheet(_sheet, titles)
                sheets.append(_sheet)
                workbooks.append(_workbook)
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
        workbook_index = 1
        for workbook in workbooks:
            workbook.save('{}/{}_{}_市级_{}.xls'.format(tag_path, tag_id, keyword, workbook_index))
            workbook_index += 1

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
    pack = Pack(data, '/Users/wangyao/Desktop/Result', 'python', 'FeedIndex')
    print('OK!')
    # count = 0
    # for i in data['City']:
    #     count += len(data['City'][i]['all'])
    # print(count)



