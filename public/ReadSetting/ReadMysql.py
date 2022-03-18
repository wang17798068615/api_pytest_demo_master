import pymysql

from configparser import ConfigParser
from api_pytest_demo_master.data.base_data import MYSQL_PATH

# 增删改查数据库方法
from api_pytest_demo_master.public.request_util.Mylogger import logger


class ReadMysql:
    conf = ConfigParser()

    conf.read(MYSQL_PATH, encoding="utf-8")

    def __init__(self):

        host = self.conf.get('mysql', 'host')  # 数据库的ip地址
        user = self.conf.get('mysql', 'user')  # 数据库的账号
        password = self.conf.get('mysql', 'password')  # 数据库的密码
        port = self.conf.getint('mysql', 'port')  # mysql数据库的端口号
        self.mysql = pymysql.connect(host=host, user=user, password=password, port=port, charset="utf8",
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.mysql.cursor()

    def GetCount(self, use_database, sql):
        """

        :param use_database: 例："use futureloan"
        :param sql: 例："select * from member where mobile_phone='13927427491';"
        :return:
        """
        try:
            # 进入所有数据库中的某一个数据库
            if use_database:
                self.cursor.execute(use_database)
            else:
                logger.error("\n注意！没有填写进入数据库命令，sql语句执行未生效")
            # 输入sql语句
            count = self.cursor.execute(sql)
            logger.info("\n数据库查询共有多少条数据方法的值为:\n{}".format(count))
            return count
        except Exception as e:
            logger.error("\n数据库查询共有多少条数据方法失败:\n", e)
            print("数据库查询共有多少条数据方法失败:", e)
        self.dataClose()

    def GetQuery(self, use_database, sql):
        """

        :param use_database: 例："use futureloan"
        :param sql: 例："select * from member where mobile_phone='13927427491';"
        :return:
        """
        try:
            # 进入所有数据库中的某一个数据库
            if use_database:
                self.cursor.execute(use_database)
            else:
                logger.error("\n注意！没有填写进入数据库命令，sql语句执行未生效")
            # 输入sql语句
            self.cursor.execute(sql)
            fetchone = self.cursor.fetchone()
            logger.info("\n数据库查询单条数据方法的值为:\n{}".format(fetchone))
            return fetchone
        except Exception as e:
            logger.error("\n数据库查询单条数据方法失败:\n", e)
            print("数据库查询单条数据方法失败:", e)
        self.dataClose()

    def GetQuerys(self, use_database, sql):
        """

        :param use_database: 例："use futureloan"
        :param sql: 例："select * from member where mobile_phone='13927427491';"
        :return:
        """
        try:
            # 进入所有数据库中的某一个数据库
            if use_database:
                self.cursor.execute(use_database)
            else:
                logger.error("\n注意！没有填写进入数据库命令，sql语句执行未生效")
            # 输入sql语句
            self.cursor.execute(sql)
            fetchall = self.cursor.fetchall()
            logger.info("\n数据库查询多条数据方法的值为:\n{}".format(fetchall))
            return fetchall
        except Exception as e:
            logger.error("\n数据库查询多条数据方法失败:\n", e)
            print("数据库查询多条数据方法失败:", e)
        self.dataClose()

    def GetQuerySize(self, use_database, sql, size=None):
        """

        :param use_database: 例："use futureloan"
        :param sql: 例："select * from member where mobile_phone='13927427491';"
        :param size:  行数 数字int类型
        :return:
        """
        try:
            # 进入所有数据库中的某一个数据库
            if use_database:
                self.cursor.execute(use_database)
            else:
                logger.error("\n注意！没有填写进入数据库命令，sql语句执行未生效")
            # 输入sql语句
            self.cursor.execute(sql)
            if size:
                fetchmany = self.cursor.fetchmany(size=size)
                logger.info("\n数据库查询指定行数数据方法的值为:\n{}".format(fetchmany))
                return fetchmany
            else:
                logger.error("\n请输入数据库查询指定行数：size=数字int类型！")
                return "请输入数据库查询指定行数：size=数字int类型！"
        except Exception as e:
            logger.error("\n数据库查询指定行数数据方法失败:\n", e)
            print("数据库查询指定行数数据方法失败:", e)
        self.dataClose()

    def update_data(self, pre_sql):
        """

        :param pre_sql: 例：'{"use_database":"use futureloan","sql":"update member set 列名称=新值 where mobile_phone='13927427491';"}'
        :return:
        """
        try:
            pre_sql_dict = eval(pre_sql)
            # 进入所有数据库中的某一个数据库
            if pre_sql_dict["use_database"]:
                self.cursor.execute(pre_sql_dict["use_database"])
            else:
                logger.error("\n注意！没有填写进入数据库命令，sql语句执行未生效")
            # 输入sql语句
            self.cursor.execute(pre_sql_dict["sql"])
        except Exception as e:
            # 如果发生错误则回滚
            logger.error("\n数据库插入/更新/删除数据方法失败:\n", e)
            print("数据库插入/更新/删除数据方法失败:", e)
            self.mysql.rollback()
        else:
            # 提交数据库执行
            self.mysql.commit()
        self.dataClose()

    # 关闭数据库方法
    def dataClose(self):
        self.cursor.close()
        self.mysql.close()


if __name__ == '__main__':
    d = ReadMysql()
    # a = d.GetQuerySize("select * from member;",2)
    # print(a)  # 0

