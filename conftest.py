# coding=utf-8
import time

import pytest
import os
import shutil

from api_pytest_demo_master.public.ReadSetting.ReadXlsx import ReadXlsx
from api_pytest_demo_master.public.request_util.Mylogger import logger

from api_pytest_demo_master.public.request_util.Variable import Variable
from api_pytest_demo_master.data.base_data import ALLUREREPORT_PATH, REQUESTLOG_PATH, HTML_PATH, DATACESHIYONGLI_PATH

from api_pytest_demo_master.public.request_util.baseapi import baseapi


@pytest.fixture(scope="session", autouse=True)
def global_init():
    # 删除request.log文件
    res = baseapi().count_dir_file(file_path=REQUESTLOG_PATH)
    if res:
        logger.warning("\n删除request.log文件")
        os.remove(REQUESTLOG_PATH)
    else:
        logger.warning("\n当前没有request.log文件，无法删除！")

    # 删除request.html文件
    logger.warning("\n删除request.html文件")
    res = baseapi().count_dir_file(file_path=HTML_PATH)
    if res:
        os.remove(HTML_PATH)
    else:
        logger.warning("\n当前没有request.html文件，无法删除！")

    # 全局变量
    logger.warning("设置全局变量")
    global_variable = ReadXlsx(DATACESHIYONGLI_PATH).getListDictRowsXlsx(name="全局变量")
    if global_variable:
        for variable in global_variable:
            setattr(Variable, variable["key"], str(variable["value"]))
            logger.warning(f"设置Variable全局变量的key值为{variable['key']},\nvalue值为:\n{variable['value']}")

    # # 普通用户
    # for user in Variable.global_user:
    #     res = is_exist_phone(user)
    #     if not res:
    #         logger.info("全局使用普通帐号 {} 不存在。现在注册一个普通用户".format(user))
    #         # 调用注册方法
    #         req_data = {"mobile_phone": user, "pwd": "12345678", "type": 1}
    #         res = SendRequests().doRequest(method="post", api_url="/member/register", json=req_data)
    #         logger.info("注册普通用户结果状态码为：{}".format(res.status_code))
    #
    # # 管理用户
    # for user in Variable.global_admin:
    #     res = is_exist_phone(user)
    #     if not res:
    #         logger.info("全局使用管理帐号 {} 不存在。现在注册一个管理用户".format(user))
    #         # 调用注册方法
    #         req_data = {"mobile_phone": user, "pwd": "12345678", "type": 0}
    #         res = SendRequests().doRequest(method="post", api_url="/member/register", json=req_data)
    #         logger.info("注册管理用户结果状态码为：{}".format(res.status_code))


# 配置局部变量
@pytest.fixture(scope="class")
def var_class_init():
    # 实例化Variable类对象，作为每一个测试类的类级别的变量。
    var_class = Variable()
    yield var_class
