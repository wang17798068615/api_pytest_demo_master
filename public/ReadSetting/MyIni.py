# coding=utf-8
from configparser import ConfigParser

from api_pytest_demo_master.data.base_data import LOG_PATH, HOST_PATH, MYSQL_PATH, USER_PATH


class MyIni:

    def __init__(self, filename):
        self.filename = filename
        self.conf = ConfigParser()
        self.conf.read(filename, encoding="utf-8")

    # 读取文件
    def ReadIni(self, section, option):
        """
        :param section:
        :param option:
        :return:
        """
        result = self.conf.get(section, option)
        return result

    # 写入追加文件
    def WriteIni(self, section, option, name):
        """
        :param section:
        :param option:
        :return:
        """

        # 设置_写入追加/覆盖section里面的option值
        self.conf.set(section, option, name)  # 写入中文
        # 设置之后必须设置文件格式:r追加/覆盖（非中文），r+追加/覆盖（中文）
        self.conf.write(open(self.filename, "r+", encoding="utf-8"))  # r+模式


if __name__ == "__main__":
    name = MyIni(LOG_PATH).ReadIni("log","name")
    # host = ReadIni(HOST_PATH, "server", "host")
    # mysql = ReadIni(MYSQL_PATH, "mysql", "host")
    # user = MyIni(USER_PATH).ReadIni("normal", "user")
    # MyIni(USER_PATH).WriteIni("normal", "user", "中文")
    print(name)
    # print(host)
    # print(mysql)
    # print(user)
    # WriteIni_a(USER_PATH)
