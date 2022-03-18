import json

import allure
import pytest

from api_pytest_demo_master.setup_case.setup_case import setup_case
from api_pytest_demo_master.data.base_data import DATACESHIYONGLI_PATH, LOG_PATH
from api_pytest_demo_master.public.ReadSetting.ReadXlsx import ReadXlsx

data = ReadXlsx(DATACESHIYONGLI_PATH).getListDictRowsXlsx(name="充值接口")


@pytest.mark.recharge
@allure.feature("充值接口")
class TestRecharge:

    @allure.title("/member/recharge")
    @pytest.mark.parametrize("case", data)
    def test_recharge(self, case, var_class_init):
        setup_case(case, var_class_init)
