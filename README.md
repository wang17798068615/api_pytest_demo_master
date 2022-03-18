### 设计说明

**API Object**是**Page Object**设计模式在接口测试上的一种延伸，顾名思义，这里是将各种基础接口进行了一层抽象封装，将其作为object，通过不同的API对象调用来组装成不同的业务流场景。因为ui自动化测试面临较多变更，所以Page Object模式的价值比较大，而如果是针对单接口的简单接口测试，其实接口层相对稳定，封装po的价值并不明显。

但是，实际项目中往往不仅是需要单接口自动化测试，更多且更有价值的是业务流的接口自动化测试，而业务流的接口测试，通常一个业务会有很多的接口依赖和调用，并且有些接口会有非常多的http协议字段填充，比如各种`headers`、`token`以及默认字段；有些接口会反复调用，比如提现业务中会调用获取账户id的接口，充值业务中也会涉及到获取账户id的接口；有些接口会有较多的处理，比如加解密等。而针对这些情况，尤其是当项目接口越来越多，业务越来越繁杂，API Object的优势就凸显出来了。（下面以一个贷款项目详细说明）

### 技术栈

- python
- requests
- pytest
- Excel
- allure

### 分层设计

整个框架分为五层：`Base层`、`接口层`、`业务层`、`用例层`、`数据层`。

如图所示：
![](http://tiebapic.baidu.com/forum/pic/item/6f0a4dd6912397dd40fe56ed1c82b2b7d1a2870c.jpg)

继承关系：用例层-->业务层-->Base层-->接口层。

调用关系：用例层（从数据层拿测试数据）-->业务层-->Base层-->接口层。

#### 接口层

接口层是对所有基础单接口的封装，负责http协议的填充。


*Utils.py*

```python
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
        # 1、从excel中读取的提取表达式，转成字典对象
        extract_dict = eval(extract)

        # 汇总全局变量
        attr = {}

        # 2、遍历1中字典的key,value.key是全局变量名，value是expr表达式。
        for key, value in extract_dict.items():
            # 根据expr从响应结果当中，提取真正的值。value就是expr表达式
            logger.info("\n导出的变量名是：\n{}\n导出的expr表达式是：\n{}".format(key, value))
            res = jsonpath.jsonpath(response_dict, value)
            if res:
                if isinstance(res, list):
                    result = res[0]
                    logger.info("\nexpr导出之后的值为:\n{}".format(result))
                    # expr找了就是列表，找不到返回False
                    # 如果提取到了真正的值，那么将它设置为Data类的属性。key是全局变量名，result[0]就是提取后的值
                    setattr(var_class_obj, key, str(result))
                    logger.info("\n导出变量名并设置var变量的key值是：\n{}\n导出expr表达式并设置var变量的value值是：{}".format(key, str(result)))

                    # 汇总局部变量
                    for key, value in var_class_obj.__dict__.items():
                        attr.update({key: value})

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
```

#### Base层

**baseapi**用于封装通用的接口流程方法，它代表的是通用接口的封装，用于跟各个api object提供支持，如提供发送http请求、读取yaml文件、替换数据等公共方法，而无关业务逻辑。

```python
# coding=utf-8
from api_pytest_demo_master.data.base_data import DATACESHIYONGLI_PATH
from api_pytest_demo_master.public.ReadSetting.ReadXlsx import ReadXlsx
from api_pytest_demo_master.public.request_util.Utils import Utils


class baseapi(object):

    @staticmethod
    # 查看文件/文件夹是否存在
    def count_dir_file(file_path=None, dir_path=None):
        """

        :param file_path: 文件路径
        :param dir_path: 文件夹路径
        :return:
        """
        return Utils.count_dir_file(file_path=file_path, dir_path=dir_path)

    @staticmethod
    # 接口依赖
    def extract_data_from_response(extract, response_dict, var_class_obj):
        """
        从响应结果当中提取值，并设置为var类的属性。
        :param extract: excel当中extract列中的提取表达式。是一个字典形式的字符串。
                            key为全局变量名。value为expr提取表达式。
        :param response: http请求之后的响应结果。字典类型。
        :return:None
        """
        return Utils.extract_data_from_response(extract=extract, response_dict=response_dict,
                                                var_class_obj=var_class_obj)

    @staticmethod
    # 判断Variable类全局变量中的登录手机号是否已注册成功
    def is_exist_phone(phone_num):
        """
        # 得到没有注册过的手机号码。
        # 1、使用faker生成手机号码
        # 2、调用mysql数据库操作，去判断是否在数据中存在。如果不在，表示没有注册
        :param phone_num: 填写Variable类全局变量中的登录手机号。
        :return:
        """
        return Utils.is_exist_phone(phone_num=phone_num)

    @staticmethod
    # 正则表达式提取标识符之后进行替换（用例）
    def replace_ReMark(self, case_dict, var_class_obj):
        """

        :param self:
        :param case_dict: 从excel当中是读取出来的一行测试数据。为字典形式。
        :param var_class_obj: 变量类
        :return:
        """
        return Utils.replace_ReMark(self=self, case_dict=case_dict, var_class_obj=var_class_obj)

    @staticmethod
    # 正则表达式提取标识符之后进行替换（数据库）
    def replace_db_ReMark(case_db_str, var_class_obj):
        """

        :param case_db_str: 从excel当中是读取出来的数据库断言测试数据。为列表嵌套字典形式。
        :param var_class_obj: 变量类
        :return:
        """
        return Utils.replace_db_ReMark(case_db_str=case_db_str, var_class_obj=var_class_obj)

    @staticmethod
    # 读取Excel数据
    def get_xlsx(name=None, num=None):
        """

        :param name: 表名，str类型
        :param num: 索引值，int类型
        :return:
        """
        return ReadXlsx(DATACESHIYONGLI_PATH).getListDictRowsXlsx(name=name, num=num)

    @staticmethod
    # 全局请求头
    def global_headers():
        """

        :param headers: request请求头字典
        :return:
        """
        return Utils.global_headers()

    @staticmethod
    # 全局url
    def global_host():
        """

        :param host: request请求url
        :return:
        """
        return Utils.global_host()

    @staticmethod
    def SendDingTalk(at_mobiles=["17798068615", ]):
        return Utils.SendDingTalk(at_mobiles=at_mobiles)

    @staticmethod
    def SendMail(user="2470162517@qq.com", password="pszxqzwiryvedihj", host="smtp.qq.com",
                 contents=["接口自动化测试报告，请查收！", "脚本：run.py", "作者:Project", "allure报告链接地址为:",
                           "https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=20022&&no=1000729"],
                 to=['982152000@qq.com'], subject="接口自动化测试报告", attachments=None):
        """

        :param user:        用来发送邮件的邮箱
        :param password:    邮箱授权码
        :param host:        邮箱的smtp服务器地址
        :param contents:    邮箱正文，自定义        例：["Aritest测试报告", "脚本：test.air", "作者:AritestProject"] --> qq邮箱页面展示内容为换行展示（一个元素对应展示一行）
        :param to:          接收邮件的邮箱          例：多个收件人写list格式['123@qq.com','1255@qq.com']，单个收件人是str格式'1255@qq.com'
        :param subject:     邮件标题
        :param attachments: 附件地址，绝对路径       例：多个附件写list格式[r'd://log.txt', r'd://baidu_img.jpg',r"D:\AA\log.zip"]，单个附件是str格式r'd://baidu_img.jpg'  * 附件格式包括：txt，jpg，zip等等...
        :return:
        """
        return Utils.SendMail(user=user, password=password, host=host, contents=contents, to=to, subject=subject,
                              attachments=None)

    @staticmethod
    # 目录压缩zip格式
    def zipDir(dirpath, outFullName):
        """
        :param dirpath: 需要导出的文件夹路径
        :param outFullName: 导出的zip压缩包的路径(含压缩包名称，此压缩文件为绝对路径)；【例 ： r"D:\AA\log.zip"】
        :return:
        """
        return Utils.zipDir(dirpath=dirpath,outFullName=outFullName)
```

此外，`baseapi`的核心只关心api的通用逻辑（遵循职责原则），所以这里对`baseapi`做了瘦身，解耦了无关逻辑（ 比如它不需要关心yaml用哪个库，能搞定就行 ），因此将工具方法单设计模式中单一独封装到`Utils.py`模块中，`baseapi`只需调用即可。

#### 业务层

这一层，即业务流层，完成测试数据的组装并且通过调用不同的接口来实现具体业务逻辑。

所有api进行http协议填充后，发送http请求并返回response，供后续对响应结果进行相关处理。

```python
import json

import allure

from api_pytest_demo_master.public.ReadSetting.ReadMysql import ReadMysql
from api_pytest_demo_master.public.request_util.MyAssert import MyAssert
from api_pytest_demo_master.public.request_util.Mylogger import logger
from api_pytest_demo_master.public.request_util.SendRequests import SendRequests
from api_pytest_demo_master.public.request_util.baseapi import baseapi

request = SendRequests()
massert = MyAssert()


def setup_case(self, case, var_class_init):
    """

    :param self:
    :param case: 测试用例
    :param var_class_init: 变量类
    :return:
    """
    # 获取类级别局部变量
    var_class = var_class_init

    # 1、正则表达式提取标识符之后进行替换
    case = baseapi().replace_ReMark(self=self, case_dict=case, var_class_obj=var_class)

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
```

如果在测试用例中直接塞进去各种http协议的填充过程，会导致用例慢慢的丢失重心，尤其是当业务越来越繁杂后，用例会非常臃肿难以维护。测试用例还是要围绕业务进行，业务要围绕实现进行，通过分层可以让用例更优雅更简洁。

#### 数据层

测试数据（测试用例）通过`Excel`管理维护，结合`pytest.paramtrize`可以非常轻松完成数据驱动。在用例层获取Excel中的测试数据，然后将数据打包给业务层，业务层进行数据拆卸组装给到接口层，接口层再调用Utils封装的方法进行填充。这样当测试数据发生变化或者用例更新，我们将不用去更新测试代码，只需维护这份Excel表格即可。

![](http://tiebapic.baidu.com/forum/pic/item/463a2f071d950a7b95b2802d4fd162d9f3d3c90c.jpg)

### 项目结构说明

- apis ---->接口层，单接口封装
- steup_case ---->业务层，业务场景封装
- testcases  --->用例层
- public  ---->公共方法
  - Readsetting  ---->读取封装目录
    - Myini.py  ---->读取/设置ini文件
    - ReadCSV.py  ---->读取csv文件
    - ReadMysql.py  ---->读取数据库
    - ReadXlsx.py  ---->读取excel文件
    - ReadYAML.py  ---->读取yaml文件
  - request_util  ---->请求接口工具层
    - async_api.py  ---->异步接口   
    - base_api.py ---->baseapi层
    - MyAssert.py ---->断言封装
    - MyFaker.py ---->随机函数
    - MyLogger.py ---->日志
    - rsa_encrypt.py ---->RSA加密 
    - SendRequests.py ---->request请求封装   
    - socket_tcp_client.py ---->tcp客户端请求
    - utils ---->工具方法封装
    - Variable.py ---->全局变量
    
- allure_report ---->allure测试报告
- conf ---->配置文件
- data ---->测试数据
- logs --->日志
- report --->html测试报告
- conftest  --->前置条件处理
- pytest.ini  --->pytest配置文件
- README.md  --->介绍文件  
- run.py  --->测试用例运行主程序
- thread_run.py  --->并发执行测试用例运行主程序

#### 测试数据动态处理(接口依赖)

测试数据中的参数有时候不能写死，而是动态变化由上一个接口的返回值中获取的。而本框架的测试数据又都是由Excel管理，那么如何能让Excel中的测试数据“动”起来呢？如何某个接口中获取传递token呢？

本框架采用的是**re正则+replace字符串替换**技术。

举个栗子，比如在调用充值接口充值的时候，那么肯定要先拿到具体的需要充值的账户id，而账户id是由登录接口获取的，因此在构造充值测试数据时，账户id不能写死，而是以`#mark#`标记，先调用登录接口拿到账户id，然后替换掉充值接口测试数据中的变量。

在用例中调用`conftest.py`的`var_class_init()`

```python
# 配置局部变量
@pytest.fixture(scope="class")
def var_class_init():
    # 实例化Variable类对象，作为每一个测试类的类级别的变量。
    var_class = Variable()
    yield var_class
```

在用例中调用`baseapi.py`的`replace_ReMark()`

```python
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
```
### 测试报告

运行`run.py`后，当用例全部执行完毕，`allure`会自动收集测试报告到`/report/html/`中，打开`request.html`即可看到完整测试报告,另外也会将`allure`的`json`文件收集到`allure_report`文件中。

![](http://tiebapic.baidu.com/forum/pic/item/3b9f8aee76094b3672f01859b4cc7cd98c109dd3.jpg)
