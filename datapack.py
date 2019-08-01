import xlwt
import json

NAME_MAP = {'SearchIndex': '搜索指数', 'FeedIndex': '资讯指数', 'NewsIndex': '媒体指数'}

class Pack:
    def __init__(self, tag_name, tag_data, tag_path, keyword):
        """
        初始化pack对象，直接将数据导出成excel
        :param tag_name: 文件名
        :param tag_data: 目标数据
        :param tag_path: 存储源路径
        :param keyword: 关键字
        """
        self._tag_name = tag_name
        self._tag_data = tag_data
        self._tag_path = tag_path
        self._keyword = keyword  # keyword用来制作表头的字符串

    def fmt_data(self):
        # 获取索要构造的数据
        tag_data = self._tag_data
        filename = '{}.xls'.format(NAME_MAP[self._tag_name])
        filepath = '{}/{}'.format(self._tag_path, filename)
        main_workbook = xlwt.Workbook(encoding='utf-8')

    def searchIndexProcess(self):
        searchIndexData = self._tag_data['SearchIndex']
        searchIndexPath = '{}/{}/'.format(self._tag_path, )
        process_data = []
        for i in searchIndexData['all']:
            process_data.append([i['date'], i['index']])
        pc_count = 0
        for j in searchIndexData['pc']:
            process_data[pc_count].append(j['index'])
            pc_count += 1
        wise_count = 0
        for k in searchIndexData['wise']:
            process_data[wise_count].append(k['index'])
            wise_count += 1



    @staticmethod
    def data2excel(_sheetname: str, _title: list, _data: list, _workbook: xlwt.Workbook):
        # 这里获取的data应该是格式化好的符合excel结构的数据
        worksheet = _workbook.add_sheet(_sheetname)
        # 构造表的标题行
        for i in range(len(_title)):
            worksheet.write(0, i, _title[i])
        # 给表填充数据
        row = 1
        for j in range(len(_data)):
            for n in range(len(_data[j])):
                worksheet.write(j+1, n, _data[j][n])
            row += 1








