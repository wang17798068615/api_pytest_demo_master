import json

import allure
import pytest

from api_pytest_demo_master.setup_case.setup_case import setup_case
from api_pytest_demo_master.data.base_data import DATACESHIYONGLI_PATH, LOG_PATH
from api_pytest_demo_master.public.ReadSetting.ReadXlsx import ReadXlsx

data = ReadXlsx(DATACESHIYONGLI_PATH).getListDictRowsXlsx(name="增加项目")

@pytest.mark.addloan
@allure.feature("增加项目接口")
class TestLoan:

    @allure.title("/loan/add")
    @pytest.mark.parametrize("case", data)
    def test_loan(self, case, var_class_init):
        setup_case(case, var_class_init)