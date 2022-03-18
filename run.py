import pytest

from api_pytest_demo_master.public.request_util.baseapi import baseapi

try:
    pytest.main(["-s", "-v", '-W', 'ignore:Module already imported:pytest.PytestWarning', "--html=report/request.html", "--alluredir=allure_report", "--clean-alluredir"])
    # 参数--clean-alluredir：在生成新的Allure报告之前，先清除该目录
    # 参数 '-W', 'ignore:Module already imported:pytest.PytestWarning'：禁用所有 pytest 内部警告PytestCacheWarning

finally:
    baseapi().SendDingTalk()
    baseapi().SendMail()
