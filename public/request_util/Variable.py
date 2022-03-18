from api_pytest_demo_master.public.request_util.Mylogger import logger


class Variable:
    user = "15500000000"
    passwd = "12345678"
    admin = "15500000011"
    admin_pwd = "12345678"
    global_user = [user, admin]
    global_admin = [admin]
    mock_url = 'https://www.fastmock.site/mock/206dd047d2278edb07eeaf592905e74d/nmb'
    pass




if __name__ == '__main__':

    for key, value in Variable.__dict__.items():
        print(key, value)  # name

    for key, value in Variable.__dict__.items():
        print(key, value)  # name 1

