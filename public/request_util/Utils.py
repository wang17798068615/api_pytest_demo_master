# coding=utf-8
import os
import re
import time
import zipfile

import jsonpath
import yagmail
from dingtalkchatbot.chatbot import DingtalkChatbot
from faker import Faker

from api_pytest_demo_master.data.base_data import DATACESHIYONGLI_PATH
from api_pytest_demo_master.public.ReadSetting.ReadMysql import ReadMysql
from api_pytest_demo_master.public.ReadSetting.ReadXlsx import ReadXlsx
from api_pytest_demo_master.public.request_util.MyFaker import PhoneFakerMysql, StrFaker, WordFaker
from api_pytest_demo_master.public.request_util.Mylogger import logger
from api_pytest_demo_master.public.request_util.Variable import Variable


class Utils(object):
    def __init__(self):
        self.fk = Faker(locale="zh-CN")

    @staticmethod
    # 查看文件/文件夹是否存在
    def count_dir_file(file_path=None, dir_path=None):
        if file_path:
            if os.path.isfile(file_path):
                return True
            else:
                return False
        if dir_path:
            if os.path.isdir(dir_path):
                return True
            else:
                return False

    @staticmethod
    # 接口依赖
    def extract_data_from_response(extract, response_dict, var_class_obj: Variable):
        extract_dict = eval(extract)
        # 全局变量
        attr = {}

        for key, value in extract_dict.items():
            logger.info("\n导出的变量名是：\n{}\n导出的expr表达式是：\n{}".format(key, value))
            res = jsonpath.jsonpath(response_dict, value)
            if res:
                if isinstance(res, list):
                    result = res[0]
                    logger.info("\nexpr导出之后的值为:\n{}".format(result))
                    setattr(var_class_obj, key, str(result))
                    logger.info("\n导出变量名并设置var变量的key值是：\n{}\n导出expr表达式并设置var变量的value值是：{}".format(key, str(result)))

                    for key, value in var_class_obj.__dict__.items():
                        attr.update({key: value})
            else:
                logger.error("\n通过extract中的expr表达式没有找到值，返回列表值为空，expr表达式为\n{}".format(value))

        logger.info("\n当前动态全局变量有:\n{}".format(attr))

    @staticmethod
    # 判断Variable类全局变量中的登录手机号是否已注册成功
    def is_exist_phone(phone_num):
        pre_sql = {"use_database": "use futureloan",
                   "sql": "select id from member where mobile_phone='{}'".format(phone_num)}
        res = ReadMysql().GetCount(use_database=pre_sql["use_database"], sql=pre_sql["sql"])
        if res == 0:
            return False
        else:
            return True

    @staticmethod
    # 正则表达式提取标识符之后进行替换（用例）
    def replace_ReMark(case_dict: dict, var_class_obj: Variable):
        case_str = str(case_dict)

        to_be_replaced_marks_list = re.findall('#(.+?)#', case_str)

        if to_be_replaced_marks_list:
            logger.warning("\n当前接口有需要进行替换的mark标识符,re表达式提取mark标识符进行替换的列表值有:\n{}".format(to_be_replaced_marks_list))

            if "phone" in to_be_replaced_marks_list:
                new_phone = PhoneFakerMysql()
                logger.info("\n有#phone#标识符，需要生成随机的手机号码为: \n{}".format(new_phone))
                case_str = case_str.replace(f"#phone#", new_phone)

            if "datetime" in to_be_replaced_marks_list:
                datetime = time.strftime("%Y-%m-%d-%H-%M-%S")  # 2021-05-22-17-30-01
                logger.info("\n有#datetime#标识符，需要生成随机的日期为: \n{}".format(datetime))
                case_str = case_str.replace(f"#datetime#", str(datetime))

            if "random_str" in to_be_replaced_marks_list:
                random_str = StrFaker()
                logger.info("\n有#random_str#标识符，需要生成20个随机的字符串为: \n{}".format(random_str))
                case_str = case_str.replace(f"#random_str#", random_str)

            if "word" in to_be_replaced_marks_list:
                word = WordFaker()
                logger.info("\n有#word#标识符，需要生成随机的词语为: \n{}".format(word))
                case_str = case_str.replace(f"#word#", word)

            mark_none = []

            for mark in to_be_replaced_marks_list:

                if hasattr(var_class_obj, mark):
                    logger.info("\n将标识符 \n{} \n替换为 \n{}".format(mark, getattr(var_class_obj, mark)))

                    case_str = case_str.replace(f"#{mark}#", getattr(var_class_obj, mark))
                else:
                    mark_none.append(mark)
                logger.info("\n当前接口用例替换之后的数据为： \n{}".format(case_str))
                logger.error("\n当前接口的标识符mark，不存在于Variable全局变量列表中，无法进行替换，不存在的标识列表值为:\n{}".format(mark_none))


        else:
            logger.warning("\n当前接口没有需要进行替换的mark标识符,re表达式提取mark标识符进行替换的列表值为空:\n{}".format(to_be_replaced_marks_list))

        new_case_dict = eval(case_str)
        return new_case_dict

    @staticmethod
    # 正则表达式提取标识符之后进行替换（数据库）
    def replace_db_ReMark(case_db_str: str, var_class_obj: Variable):
        to_be_replaced_marks_list = re.findall('#(.+?)#', case_db_str)

        if to_be_replaced_marks_list:
            logger.warning(
                "\n当前接口中的assert_db有需要进行替换的mark标识符,re表达式提取mark标识符进行替换的列表值有:\n{}".format(to_be_replaced_marks_list))

            mark_none = []

            for mark in to_be_replaced_marks_list:

                if hasattr(var_class_obj, mark):
                    logger.info("\n将标识符 \n{} \n替换为 \n{}".format(mark, getattr(var_class_obj, mark)))

                    case_db_str = case_db_str.replace(f"#{mark}#", getattr(var_class_obj, mark))
                else:
                    mark_none.append(mark)
                logger.info("\n当前接口用例替换之后的数据为： \n{}".format(case_db_str))
                logger.error("\n当前接口的标识符mark，不存在于Variable全局变量列表中，无法进行替换，不存在的标识列表值为:\n{}".format(mark_none))

        else:
            logger.warning(
                "\n当前接口中的assert_db没有需要进行替换的mark标识符,re表达式提取mark标识符进行替换的列表值为空:\n{}".format(to_be_replaced_marks_list))

        return case_db_str

    @staticmethod
    # 全局请求头
    def global_headers():
        re_dict = {}
        global_headers = ReadXlsx(DATACESHIYONGLI_PATH).getListDictRowsXlsx(name="全局请求头")
        if global_headers:
            flag = False
            # 将请求头设置为全局请求头
            dict = {}
            for var in global_headers:
                dict[var["key"]] = var["value"]
                re_dict.update(dict)
                flag = True
            if not flag:
                logger.warning(f"\n没有全局请求头，全局请求头保留空字典格式，为\n{re_dict}")
        return re_dict

    @staticmethod
    # 全局url
    def global_host():
        host = None
        global_host = ReadXlsx(DATACESHIYONGLI_PATH).getListDictRowsXlsx(name="全局路径")
        if global_host:
            flag = False
            # 将路径设置为全局路径
            for var in global_host:
                host = var["value"]
                flag = True
            if not flag:
                logger.error(f"\n没有全局请求路径，全局请求路径保留空字典格式，为\n{host}")
        return host

    @staticmethod
    # 发送钉钉
    def SendDingTalk(at_mobiles=None):
        webhook = "https://oapi.dingtalk.com/robot/send?access_token=b4c54f4298191a91b32be9941f14410f0bdabec4ef3ed7f20245004333804ec9"
        secret = "SEC817c602fb46721d499b396b3f19a5b39226646fd6a2e339f937ac86ca461d234"

        # 初始化机器人小丁
        xiaoding = DingtalkChatbot(webhook, secret, pc_slide=False, fail_notice=True)  # 方式一：通常初始化方式

        # Link消息(无法@指定用户)
        # xiaoding.send_link(title=title, text=text, message_url=message_url, pic_url=pic_url)

        # Markdown消息@指定用户
        xiaoding.send_markdown(title="接口自动化测试报告", text='接口自动化测试报告，请查收！\n'
                                                       '> ![美景](http://www.sinaimg.cn/dy/slidenews/5_img/2013_28/453_28488_469248.jpg)\n'
                                                       '> ###### [allure报告链接地址](http://www.thinkpage.cn/) \n',
                               at_mobiles=at_mobiles)

    @staticmethod
    # 发送邮箱
    def SendMail(user=None, password=None, host=None, contents=None, to=None, subject=None, attachments=None):
        user = user
        password = password
        host = host
        contents = contents
        to = to
        subject = subject
        attachments = None
        try:
            # 连接邮箱服务器 【由于通过yagmail发送文件，文件名会乱码，设置SMTP格式为即可：encoding="GBK"】
            yag = yagmail.SMTP(user=user, password=password, host=host, encoding="GBK")

            # 邮箱正文，自定义
            contents = contents

            # 发送邮箱
            yag.send(to=to, subject=subject, contents=contents, attachments=attachments, )
        except  Exception as e:
            print("发送邮箱方法失败:", e)

    @staticmethod
    # 目录压缩zip格式
    def zipDir(dirpath, outFullName):
        try:
            zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)

            for path, dirnames, filenames in os.walk(dirpath):

                fpath = path.replace(dirpath, "")

                for filename in filenames:
                    zip.write(os.path.join(path, filename), os.path.join(fpath, filename))

            zip.close()
        except Exception as e:
            print("目录压缩zip格式方法失败:", e)
