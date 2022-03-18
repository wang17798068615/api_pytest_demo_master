import json

import allure

from api_pytest_demo_master.public.ReadSetting.ReadMysql import ReadMysql
from api_pytest_demo_master.public.request_util.MyAssert import MyAssert
from api_pytest_demo_master.public.request_util.Mylogger import logger
from api_pytest_demo_master.public.request_util.SendRequests import SendRequests
from api_pytest_demo_master.public.request_util.baseapi import baseapi

request = SendRequests()
massert = MyAssert()


def setup_case(case, var_class_init):
    """

    :param self:
    :param case: 测试用例
    :param var_class_init: 变量类
    :return:
    """
    # 获取类级别局部变量
    var_class = var_class_init

    # 1、正则表达式提取标识符之后进行替换
    case = baseapi().replace_ReMark(case_dict=case, var_class_obj=var_class)

    # 2、执行前置sql
    if case.get("pre_sql"):
        ReadMysql().update_data(case["pre_sql"])
    else:
        logger.warning("\n前置sql列为空，不进行当前接口前置sql之pre_sql]操作！")

    # 3、把替换之后的请求数据(json格式的字符串)，转换成一个字典
    req_dict = json.loads(case["req_data"])

    # 4、发起请求，并接收响应结果
    if hasattr(var_class, "token"):
        response = SendRequests().doRequest(method=case["method"], api_url=case["url"], json=req_dict,
                                            token=getattr(var_class, "token"))
    elif case.get("headers"):
        response = SendRequests().doRequest(method=case["method"], api_url=case["url"], json=req_dict,
                                            headers=case["headers"])

    elif hasattr(var_class, "token") and case.get("headers"):
        response = SendRequests().doRequest(method=case["method"], api_url=case["url"], json=req_dict,
                                            token=getattr(var_class, "token"), headers=case["headers"])
    else:
        response = SendRequests().doRequest(method=case["method"], api_url=case["url"], json=req_dict)

    # 断言结果空列表
    assert_res = []

    # 5、断言响应结果中的数据
    if case.get("assert_list"):
        response_check_res = massert.assert_response_value(case["assert_list"], response)
        assert_res.append(response_check_res)
    else:
        logger.warning("\n响应断言列为空，不进行当前接口响应断言assert_list操作！")

    # 6、提取响应结果中的数据,并设置为全局变量
    if case.get("extract"):
        # 判断当前接口是否为False(如果是False表明当前接口返回数据有问题，不能进行导出extract操作)
        if False not in assert_res:
            # 调用提取处理函数
            baseapi().extract_data_from_response(case["extract"], response.json(), var_class_obj=var_class)
        else:
            logger.warning("\n当前接口响应断言列assert_list断言失败，无法进行extract导出提取操作，响应断言列结果为:\n{}".format(assert_res))
    else:
        logger.warning("\n导出提取列为空，不进行当前接口导出提取extract操作！")

    # 7、断言数据库 - sql语句结果与实际比对的类型（先extract提取相应返回数据设置全局变量，再根据当前接口的返回数据，编写对应的sql进行查询断言！）
    if case.get("assert_db"):
        # 如果case["assert_db"]中有#标识，代表需要依赖当前接口返回数据去进行sql查询断言（此操作会影响效率自动化执行效率，延长全局变量释放时间,其实延长不了多少时间~）
        if case["assert_db"].find("#") != -1:
            case["assert_db"] = baseapi().replace_db_ReMark(case_db_str=case["assert_db"], var_class_obj=var_class)
        # 断言数据库
        db_check_res = massert.assert_db(case["assert_db"])
        assert_res.append(db_check_res)
    else:
        logger.warning("\n数据库断言列为空，不进行当前接口数据库断言assert_db操作！")

    # 8.最终的抛AsserttionError
    if False in assert_res:
        # 如果响应断言失败
        if False == assert_res[0]:
            logger.error(f"\n当前接口{case.get('url')},第{case.get('id')}条用例执行响应断言列assert_list断言失败")
            allure.attach(body=f"当前接口{case.get('url')}第{case.get('id')}条用例执行响应断言失败", name="当前接口响应断言失败",
                          attachment_type=allure.attachment_type.TEXT)
        # 如果数据库言失败
        if False == assert_res[1]:
            logger.error(f"\n当前接口{case.get('url')}第{case.get('id')}条用例执行数据库断言失败")
            allure.attach(body=f"当前接口{case.get('url')}第{case.get('id')}条用例执行数据库断言失败", name="当前接口数据库断言失败",
                          attachment_type=allure.attachment_type.TEXT)
        allure.attach(body=f"{assert_res}", name="当前接口的响应断言和数据库断言列为",
                      attachment_type=allure.attachment_type.TEXT)
        raise AssertionError
    else:
        logger.info("当前所有接口用例断言通过！")
        allure.attach(body=f"{assert_res}", name="当前所有接口用例断言通过，响应断言和数据库断言列为",
                      attachment_type=allure.attachment_type.TEXT)
