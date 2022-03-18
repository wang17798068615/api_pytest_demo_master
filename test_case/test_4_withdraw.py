import json

import allure
import pytest

from api_pytest_demo_master.setup_case.setup_case import setup_case
from api_pytest_demo_master.data.base_data import DATACESHIYONGLI_PATH, LOG_PATH
from api_pytest_demo_master.public.ReadSetting.ReadXlsx import ReadXlsx

data = ReadXlsx(DATACESHIYONGLI_PATH).getListDictRowsXlsx(name="提现接口")

@pytest.mark.withdraw
@allure.feature("提现接口")
class TestWithdraw:

    @allure.title("/member/withdraw")
    @pytest.mark.parametrize("case", data)
    def test_withdraw(self, case, var_class_init):
        setup_case(case, var_class_init)