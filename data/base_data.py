import os

HOST = "http://api.lemonban.com/futureloan"

auto_data = os.path.split(os.path.realpath(__file__))[0]

auto = os.path.dirname(auto_data)

LOG_PATH = os.path.join(auto, "conf", "log.ini")
HOST_PATH = os.path.join(auto, "conf", "host.ini")
MYSQL_PATH = os.path.join(auto, "conf", "mysql.ini")
USER_PATH = os.path.join(auto, "conf", "user.ini")
PYTEST_PATH = os.path.join(auto, "pytest.ini")

LOGGER_PATH = os.path.join(auto, "logs")
REQUESTLOG_PATH = os.path.join(auto, "logs","request.log")

ALLUREREPORT_PATH = os.path.join(auto, "allure_report")
HTML_PATH = os.path.join(auto, "report","request.html")

CONFIGZHUCELOGINYAML_PATH = os.path.join(auto, "config", "zhuCeLogin.yaml")
DATACESHIYONGLI_PATH = os.path.join(auto_data, "测试用例.xlsx")

DATA_PATH = os.path.join(auto_data, "data.csv")