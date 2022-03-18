import concurrent.futures
from time import sleep

import pytest
import os

from api_pytest_demo_master.data.base_data import PYTEST_PATH
from api_pytest_demo_master.public.ReadSetting.MyIni import MyIni
from api_pytest_demo_master.public.request_util.Mylogger import logger
from api_pytest_demo_master.public.request_util.baseapi import baseapi

"""
每个表单下的用例是一个任务。有多少个表单就有多少个任务。

1、pytest.ini 中添加标记
2、测试类添加标记
"""
pytest.main(['-W', 'ignore:Module already imported:pytest.PytestWarning', "--clean-alluredir"])
# 所有的标签名字读取出来、意味着有多少个任务
markers_str = MyIni(PYTEST_PATH).ReadIni("pytest", "markers")
marks = markers_str.split("\n")[1::]
print(marks)


# 定义一个方法。此方法用来收集每个接口的测试用例，并执行它。
# 需要事先准备：接口名称（将每个接口依次进行pytest,mark标记，执行时并发时，将依次执行mark标记）
def run_cases(mark_name):
    pytest.main(["-s", "-v", '-W', 'ignore:Module already imported:pytest.PytestWarning', "-m", f"{mark_name}",
                 "--html=report/request.html", "--alluredir=allure_report"])


# 并发执行5个接口（有序执行）
# 1、设置线程池数目：
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_cases = {}
    # 提交子任务
    for mark in marks:
        # 2、使用 submit 函数来提交线程需要执行的任务到线程池中，并返回该任务的句柄：
        task = executor.submit(run_cases, mark)
        future_to_cases[task] = mark
        # 如果并发执行接口自动化失败，添加5秒等待即可!
        sleep(5)

    logger.info("\n使用 submit 函数,返回该任务的句柄为：", future_to_cases)
    # 等待子任务完成
    for future in concurrent.futures.as_completed(future_to_cases):
        try:
            res = future.result()
            logger.info(f"\n{res}")
        except Exception as exc:
            logger.error('generated an exception: %s' % exc)
baseapi().SendDingTalk()
baseapi().SendMail()
