import ast
import json
from datetime import datetime
from decimal import Decimal

import allure
import jsonpath

from api_pytest_demo_master.public.ReadSetting.ReadMysql import ReadMysql
from api_pytest_demo_master.public.request_util.Mylogger import logger


class MyAssert:

    def assert_response_value(self, assert_list, response):
        """
        :param assert_list: 从excel当中，读取出来的断言列。是一个列表形式的字符串。里面的成员是一个断言
        :param result: 接口请求结果
        :return: None
        """
        with allure.step('发送请求'):
            allure.attach(str(response.request.url), '请求路径', attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.request.method), '请求方式', attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.request.headers), '请求头', attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.request.body), '请求体', attachment_type=allure.attachment_type.TEXT)

        with allure.step('获取响应'):
            allure.attach(str(response.status_code), '响应状态码', attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.headers), '响应头', attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.text), '响应文本内容', attachment_type=allure.attachment_type.TEXT)

        # 所有断言的比对结果列表
        check_res = []

        # 把字符串转换成python列表
        check_list = eval(assert_list)

        for check in check_list:

            logger.info("\n要断言的内容为：\n{}".format(check))
            # 通过jsonpath表达式，从响应结果当中拿到了实际结果
            res = jsonpath.jsonpath(response.json(), check["expr"])
            if res:
                if isinstance(res, list):
                    result_jsonpath = res[0]

                    logger.info("\n从响应结果当中，提取到的值为:\n{}".format(result_jsonpath))
                    logger.info("\n期望结果为:\n{}".format(check["expected"]))

                    # 根据type来调用不同的方法来执行sql语句。
                    if check["type"] == "eq":
                        logger.info("\n比对2个值是否相等。")
                        logger.info("\n比对结果为：\n{}".format(result_jsonpath == check["expected"]))
                        check_res.append(result_jsonpath == check["expected"])

                        with allure.step('响应断言'):
                            allure.attach(str(result_jsonpath), '实际响应结果', attachment_type=allure.attachment_type.TEXT)
                            allure.attach(str(check["expected"]), '预期响应结果', attachment_type=allure.attachment_type.TEXT)

                    elif check["type"] == "not_eq":
                        logger.info("\n比对2个值是否相等。")
                        logger.info("\n比对结果为：\n{}".format(result_jsonpath != check["expected"]))
                        check_res.append(result_jsonpath != check["expected"])

                        with allure.step('响应断言'):
                            allure.attach(str(result_jsonpath), '实际响应结果', attachment_type=allure.attachment_type.TEXT)
                            allure.attach(str(check["expected"]), '预期响应结果', attachment_type=allure.attachment_type.TEXT)

                    elif check["type"] == "is":
                        logger.info("\n比对2个值是否相等。")
                        logger.info("\n比对结果为：\n{}".format(result_jsonpath is check["expected"]))
                        check_res.append(result_jsonpath is check["expected"])

                        with allure.step('响应断言'):
                            allure.attach(str(result_jsonpath), '实际响应结果', attachment_type=allure.attachment_type.TEXT)
                            allure.attach(str(check["expected"]), '预期响应结果', attachment_type=allure.attachment_type.TEXT)

                    elif check["type"] == "is_not":
                        logger.info("\n比对2个值是否相等。")
                        logger.info("\n比对结果为：\n{}".format(result_jsonpath is not check["expected"]))
                        check_res.append(result_jsonpath is not check["expected"])

                        with allure.step('响应断言'):
                            allure.attach(str(result_jsonpath), '实际响应结果', attachment_type=allure.attachment_type.TEXT)
                            allure.attach(str(check["expected"]), '预期响应结果', attachment_type=allure.attachment_type.TEXT)

                    elif check["type"] == "in":
                        logger.info("\n比对2个值是否相等。")
                        logger.info("\n比对结果为：\n{}".format(result_jsonpath in check["expected"]))
                        check_res.append(result_jsonpath in check["expected"])

                        with allure.step('响应断言'):
                            allure.attach(str(result_jsonpath), '实际响应结果', attachment_type=allure.attachment_type.TEXT)
                            allure.attach(str(check["expected"]), '预期响应结果', attachment_type=allure.attachment_type.TEXT)

                    elif check["type"] == "not_in":
                        logger.info("\n比对2个值是否相等。")
                        logger.info("\n比对结果为：\n{}".format(result_jsonpath not in check["expected"]))
                        check_res.append(result_jsonpath not in check["expected"])

                        with allure.step('响应断言'):
                            allure.attach(str(result_jsonpath), '实际响应结果', attachment_type=allure.attachment_type.TEXT)
                            allure.attach(str(check["expected"]), '预期响应结果', attachment_type=allure.attachment_type.TEXT)

                    else:
                        logger.error("\n不支持的响应断言比对类型！请检查你的断言写法！")
                        allure.attach(body='不支持的响应断言比对类型！请检查你的断言写法！', name='不支持的响应断言比对类型！',
                                      attachment_type=allure.attachment_type.TEXT)
                        raise Exception
            else:
                logger.error("\n通过extract中的jsonpath表达式没有找到值，返回列表值为空，jsonpath表达式为\n{}".format(check["expr"]))

        if False in check_res:
            # raise AssertionError
            return False
        else:
            return True

    def assert_db(self, check_db_str):
        """
        1、将check_db_str转成python对象(列表)，通过eval
        2、遍历1中的列表，访问每一组db比对
        3、对于每一组来讲，1）调用数据库类，执行sql语句。调哪个方法，根据type来决定。得到实际结果
                       2）与期望结果比对
        :param check_db_str: 测试数据excel当中，assert_db列读取出来的数据库检验字符串。
              示例：[{"sql":"select id from member where mobile_phone='#phone#'","expected":1,"type":"count"}]
        :return: None
        """
        # 所有断言的比对结果列表
        check_db_res = []

        # 把字符串转换成python列表
        check_db_list = eval(check_db_str)  # 比eval安全一点。转成列表。

        # 建立数据库连接
        db = ReadMysql()

        # 遍历check_db_list
        for check_db_dict in check_db_list:
            allure.attach(str(check_db_dict["sql"]), '当前要比对的sql语句', attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(check_db_dict["db_type"]), '当前执行sql的查询类型(查询结果条数/查询某个值.)',
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(check_db_dict["expected"]), '预期结果为：', attachment_type=allure.attachment_type.TEXT)

            logger.info("\n当前要比对的sql语句：\n{}".format(check_db_dict["sql"]))
            logger.info("\n当前执行sql的查询类型(查询结果条数/查询某个值.)：\n{}".format(check_db_dict["db_type"]))
            logger.info("\n预期结果为：\n{}".format(check_db_dict["expected"]))

            # 根据db_type来调用不同的方法来执行sql语句。
            # 条数比对
            if check_db_dict["db_type"] == "count":
                logger.info("\n比对数据库查询的结果条数，是否符合期望")
                # 执行sql语句
                res = db.GetCount(use_database=check_db_dict["use_database"], sql=check_db_dict["sql"])
                logger.info("\nsql的执行结果为：\n{}".format(res))

                # 将比对结果添加到结果列表当中
                check_db_res.append(res == check_db_dict["expected"])
                logger.info("\n比对结果为：\n{}".format(res == check_db_dict["expected"]))

                with allure.step('数据库断言'):
                    allure.attach(str(res), '实际sql的执行结果', attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(check_db_dict["expected"]), '预期响应结果', attachment_type=allure.attachment_type.TEXT)
            # 数据比对
            elif check_db_dict["db_type"] == "eq":
                logger.info("\n比对数据库查询出来的数据，是否与期望相等")
                # 执行sql语句
                res = db.GetQuery(use_database=check_db_dict["use_database"], sql=check_db_dict["sql"])
                logger.info("\nsql的执行结果为：\n{}".format(res))

                for key, value in res.items():
                    if isinstance(value, Decimal):
                        res[key] = float(value)
                    if isinstance(value, datetime):
                        res[key] = str(value)

                # 将比对结果添加到结果列表当中
                check_db_res.append(res == check_db_dict["expected"])
                logger.info("\n比对结果为：\n{}".format(res == check_db_dict["expected"]))

                with allure.step('数据库断言'):
                    allure.attach(str(res), '实际sql的执行结果', attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(check_db_dict["expected"]), '预期响应结果', attachment_type=allure.attachment_type.TEXT)

            else:
                logger.error("\n不支持的数据库比对类型！请检查你的断言写法！")
                allure.attach(body='不支持的数据库比对类型！请检查你的断言写法！', name='不支持的数据库比对类型！',
                              attachment_type=allure.attachment_type.TEXT)
                raise Exception

        if False in check_db_res:
            # raise AssertionError
            return False
        else:
            return True


if __name__ == '__main__':
    # 已经从excel当中读取出来的字符串
    check_db_str = """[{"use_database":"use futureloan","sql":"select id from member where mobile_phone='15500000000'","expected":1,"db_type":"count"}]"""
    res = MyAssert().assert_db(check_db_str)
    print(res)
