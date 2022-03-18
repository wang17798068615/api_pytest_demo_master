import logging
from logging import Logger

# pip install concurrent_log_handler(多线程并发日志库)
from concurrent_log_handler import ConcurrentRotatingFileHandler

from api_pytest_demo_master.data.base_data import LOG_PATH, LOGGER_PATH
from api_pytest_demo_master.public.ReadSetting.MyIni import MyIni


class Mylogger(Logger):

    def __init__(self, name=None, level=logging.INFO, filename=None):
        self.file = filename
        self.setlevel = level
        fmt = "%(asctime)s:%(name)s:%(levelname)s:%(pathname)s:%(lineno)d:%(message)s"
        formatter = logging.Formatter(fmt)
        super(Mylogger, self).__init__(name, level)
        handler1 = logging.StreamHandler()
        handler1.setFormatter(formatter)
        self.addHandler(handler1)

        if filename:
            handler2 = ConcurrentRotatingFileHandler(filename, maxBytes=20 * 1024 * 1024, backupCount=5,
                                                     encoding="utf-8")
            handler2.setFormatter(formatter)
            self.addHandler(handler2)


name = MyIni(LOG_PATH).ReadIni("log", "name")
level = MyIni(LOG_PATH).ReadIni("log", "level")
file = MyIni(LOG_PATH).ReadIni("log", "file")

logger = Mylogger(name, level, LOGGER_PATH + f"/{file}")

if __name__ == "__main__":
    logger.info("1")
