import yaml

# 获取yaml文件方法
from api_pytest_demo_master.data.base_data import CONFIGZHUCELOGINYAML_PATH


def ReadYaml(filename):
    try:
        file = open(filename, mode="r", encoding="utf-8")
        res = yaml.safe_load(file)
        return res
    except Exception as e:
        print("获取yaml文件方法失败:", e)


if __name__ == '__main__':
    res = ReadYaml(CONFIGZHUCELOGINYAML_PATH)
    # res = ReadYaml(r"D:\pycharm_workspace\proTest\api_pytest_demo_master\config\aa.yaml")
    print(res)
