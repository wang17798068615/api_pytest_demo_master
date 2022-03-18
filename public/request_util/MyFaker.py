# coding=utf-8
import time

from faker import Faker

from api_pytest_demo_master.public.request_util.Mylogger import logger
from api_pytest_demo_master.public.ReadSetting.ReadMysql import ReadMysql

fk = Faker(locale="zh-CN")


# 随机手机号
def PhoneFakerMysql(option="not_in"):
    """

    :param option: not_in 默认手机号不存在于数据库中，填写其它字符即手机号存在于数据库中
    :return:
    """
    phone = fk.phone_number()
    # phone = 13986811713  # 不存在
    # phone = 18610100022  # 存在
    pre_sql = {"use_database": "use futureloan", "sql": f"select * from member where mobile_phone='{phone}';"}
    res = ReadMysql().GetCount(use_database=pre_sql["use_database"], sql=pre_sql["sql"])
    if option == "not_in" and res == 0:
        logger.info(f"\n获取随机手机号且不存在于数据库中的值为:\n{phone}")
        return phone
    else:
        logger.info(f"\n获取随机手机号且存在于数据库中的值为:\n{phone}")
        return phone


# 判断Variable类全局变量中的登录手机号是否已注册成功
def is_exist_phone(phone_num):
    """
    :param phone_num: 填写Variable类全局变量中的登录手机号。
    :return:
    """
    pre_sql = {"use_database": "use futureloan",
               "sql": "select id from member where mobile_phone='{}'".format(phone_num)}
    res = ReadMysql().GetCount(use_database=pre_sql["use_database"], sql=pre_sql["sql"])
    if res == 0:
        return False
    else:
        return True


# 20个随机字符串
def StrFaker():
    rstr = fk.pystr()
    return rstr  # aULgvNpftEJnMkipRMKi


# 随机词语
def WordFaker():
    fk = Faker(locale="zh-CN")
    word = fk.word()
    return word  # 自己


if __name__ == '__main__':
    print(PhoneFakerMysql("sa"))
    print(type(PhoneFakerMysql("sa")))  # <class 'str'>
    rstr = StrFaker()
    print(rstr)
