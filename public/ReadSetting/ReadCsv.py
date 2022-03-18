import csv

# 读取csv文件数据_字典格式1
from api_pytest_demo_master.data.base_data import DATA_PATH


def ReadCsv1(filename):
    file = open(file=filename, mode='r', encoding='utf-8-sig')
    read = csv.DictReader(file)
    return list(read)


# 读取csv文件数据_字典格式2
def ReadCsv(filename):
    f = open(file=filename, mode='r', encoding='utf-8-sig')
    reader = list(csv.reader(f))
    # [{'csid':1,'page':1},{}]
    dictList = []
    for i in range(1, len(reader)):
        dict = {}  # 一条数据的字典
        data = reader[i]  # 一条csv数据
        keys = reader[0]  # key数据
        for j in range(len(keys)):
            dict[keys[j]] = data[j]  # 组装一条字典

        dictList.append(dict)  # 添加到列表

    return dictList


if __name__ == "__main__":
    data1 = ReadCsv(DATA_PATH)
    print(data1)
