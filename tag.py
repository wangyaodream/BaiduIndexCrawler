from urllib.parse import urlencode


class Tag:
    def __init__(self, target):
        self._target = target

    def structure_urls(self, keyword, startdate, enddate, area):
        # 这里暂时是一个单独url的测试，后续应该返回的是一个目标url的集合
        request_args = {
            'word': keyword,
            'startDate': startdate,
            'endDate': enddate,
            'area': area,
        }
        tag_urls = dict()
        # 搜索指数
        tag_urls['SearchIndex'] = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        # 资讯指数
        tag_urls['FeedIndex'] = 'http://index.baidu.com/api/FeedSearchApi/getFeedIndex?' + urlencode(request_args)
        # 媒体指数
        tag_urls['NewsIndex'] = 'http://index.baidu.com/api/NewsApi/getNewsIndex?' + urlencode(request_args)
        return tag_urls[self._target]