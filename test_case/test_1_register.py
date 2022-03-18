import json

import allure
import pytest

from api_pytest_demo_master.setup_case.setup_case import setup_case
from api_pytest_demo_master.data.base_data import DATACESHIYONGLI_PATH, LOG_PATH
from api_pytest_demo_master.public.ReadSetting.ReadXlsx import ReadXlsx

data = ReadXlsx(DATACESHIYONGLI_PATH).getListDictRowsXlsx(name="注册接口")



@pytest.mark.register
@allure.feature("注册接口")
class TestRegister:

    @allure.title("/member/register")
    @pytest.mark.parametrize("case", data)
    def test_register(self, case, var_class_init):
        setup_case(case,var_class_init)