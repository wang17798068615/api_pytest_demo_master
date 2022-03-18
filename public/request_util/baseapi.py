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
    def replace_ReMark(case_dict, var_class_obj):
        """

        :param self:
        :param case_dict: 从excel当中是读取出来的一行测试数据。为字典形式。
        :param var_class_obj: 变量类
        :return:
        """
        return Utils.replace_ReMark(case_dict=case_dict, var_class_obj=var_class_obj)

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