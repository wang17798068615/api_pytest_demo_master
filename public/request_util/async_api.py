import time
import requests


# 测试异步接口（示例）
def create_order():
    url = "http://115.28.108.130:5000/api/order/create/"  # 异步接口
    data = {
        "user_id": "1234",
        "goods_id": "136",
        "num": 10,
        "amount": 20.00
    }
    res = requests.post(url=url, data=data)
    return res.json().get("order_id")  # 返回order_id用于追踪


def get_order_result(interval=1, time_out=60):  # 设置了默认时间间隔和超时时间,可以修改
    order_id = create_order()
    # 查询结果接口
    url = "http://115.28.108.130:5000/api/order/get_result/?order_id={}".format(order_id)
    start_time = time.time()  # 启动时间
    end_time = start_time + time_out  # 启动时间+超时时间=结束时间
    count = 1  # 计数器, 此处是为了显示更直观, 可以去掉
    while time.time() < end_time:  # 当未到结束时间时, 循环请求
        res = requests.get(url)  # 请求查询结果接口
        print(count, res.json())
        count += 1
        time.sleep(interval)  # 休眠指定时间
        if res.json():  # 如果有数据则退出循环
            break
    else:
        return None  # 正常退出(达到end_time, 非break退出) 返回None
    return res.json()  # break退出返回 接口数据


if __name__ == '__main__':
    order_result = get_order_result()
    print(order_result)
