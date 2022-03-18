import allure
import requests

from api_pytest_demo_master.data.base_data import HOST_PATH, DATACESHIYONGLI_PATH
from api_pytest_demo_master.public.ReadSetting.ReadXlsx import ReadXlsx
from api_pytest_demo_master.public.request_util.Mylogger import logger
from api_pytest_demo_master.public.request_util.baseapi import baseapi
from api_pytest_demo_master.public.request_util.rsa_encrypt import generator_sign


class SendRequests:
    # 初始化方法
    def __init__(self):
        # 全局请求头（在Excel表中全局请求头表单中进行设置）
        self.headers = {}
        re_dict = baseapi.global_headers()
        self.headers.update(re_dict)

        # 全局请求路径（在Excel表中全局路径表单中进行设置）
        self.host = None
        host = baseapi.global_host()
        self.host = host

    def __doGet(self, url, params=None, **kwargs):
        result = requests.get(url=url, params=params, **kwargs)

        logger.info('\n请求路径:\n' + str(result.request.url))
        logger.info('\n请求方式:\n' + str(result.request.method))
        logger.info('\n请求头:\n' + str(result.request.headers))
        logger.info('\n请求体:\n' + str(result.request.body))
        logger.info('\n响应状态码:\n' + str(result.status_code))
        logger.info('\n响应头:\n' + str(result.headers))
        # 查看相应内容，必须通过text查看，因为通过json查看时，如果不是json格式就会报错！
        logger.info('\n响应文本内容:\n' + str(result.text))

        return result

    def __doPost(self, url, data=None, json=None, **kwargs):
        result = requests.post(url=url, data=data, json=json, **kwargs)

        logger.info('\n请求路径:\n' + str(result.request.url))
        logger.info('\n请求方式:\n' + str(result.request.method))
        logger.info('\n请求头:\n' + str(result.request.headers))
        logger.info('\n请求体:\n' + str(result.request.body))
        logger.info('\n响应状态码:\n' + str(result.status_code))
        logger.info('\n响应头:\n' + str(result.headers))
        # 查看相应内容，必须通过text查看，因为通过json查看时，如果不是json格式就会报错！
        logger.info('\n响应文本内容:\n' + str(result.text))

        return result

    def __doPut(self, url, data=None, json=None, **kwargs):
        result = requests.put(url=url, data=data, json=json, **kwargs)

        logger.info('\n请求路径:\n' + str(result.request.url))
        logger.info('\n请求方式:\n' + str(result.request.method))
        logger.info('\n请求头:\n' + str(result.request.headers))
        logger.info('\n请求体:\n' + str(result.request.body))
        logger.info('\n响应状态码:\n' + str(result.status_code))
        logger.info('\n响应头:\n' + str(result.headers))
        # 查看相应内容，必须通过text查看，因为通过json查看时，如果不是json格式就会报错！
        logger.info('\n响应文本内容:\n' + str(result.text))

        return result

    # 添加token请求头
    def __deal_header(self, token=None):
        if token:
            logger.info("\n已有的全局变量请求头为：\n{}".format(self.headers))
            self.headers["Authorization"] = "Bearer {}".format(token)
        logger.info("\n添加的token请求头为：\n{}".format(self.headers))
        logger.info("\n添加token请求头后的全局请求头为：\n{}".format(self.headers))

    # 添加多个请求头
    def __add_header(self, headers_str=None):
        if headers_str:
            logger.info("\n已有的全局变量请求头为：\n{}".format(self.headers))
            self.headers.update(eval(headers_str))
        logger.info("\n添加多个请求头为：\n{}".format(headers_str))
        logger.info("\n添加多个请求头后的全局请求头为：\n{}".format(self.headers))

    # 请求路径
    def __deal_host(self, api_url):
        # 如果是mock数据，也就是url以https或者http开头的，直接返回url
        if api_url.startswith("https://") or api_url.startswith("http://"):
            logger.info("\n当前接口是mock数据，接口url为：\n{}".format(api_url))
            return api_url
        # 如果不是mock数据，需要拼接host基础url，再进行返回url
        else:
            if not api_url.startswith("/"):
                url = self.host + api_url
                logger.info("\n请求api_url拼接后的路径为：\n{}".format(url))
                return url
            else:
                api_url = api_url.replace("/", "", 1)
                url = self.host + api_url
                logger.info("\n请求api_url拼接后的路径为：\n{}".format(url))
                return url

    def doRequest(self, method, api_url, params=None, data=None, json=None, verify=False, headers=None, token=None,
                  **kwargs):
        # verify：request请求时是否需要SSL证书，True需要，False不需要，默认为True

        # 处理token请求头
        self.__deal_header(token)
        # 处理请求路径
        url = self.__deal_host(api_url)
        # 处理多个请求头(如果添加的请求头，已存在于全局变量中，不会进行替换，不一样请求头依然还会进行添加。)
        self.__add_header(headers)

        if method.upper() == 'GET':
            return self.__doGet(url=url, params=params, headers=self.headers, verify=verify, **kwargs)

        elif method.upper() == 'POST':
            return self.__doPost(url=url, data=data, json=json, headers=self.headers, verify=verify, **kwargs)

        elif method.upper() == 'PUT':
            return self.__doPut(url=url, data=data, json=json, headers=self.headers, verify=verify, **kwargs)

        else:
            logger.error('暂时不支持的请求方式')


if __name__ == '__main__':
    logger.info("1")
    # s = SendRequests()
    # s.add_header('{"X-Lemonban-Media-Type": "lemonban.v2"}')
    # print(s.headers)
