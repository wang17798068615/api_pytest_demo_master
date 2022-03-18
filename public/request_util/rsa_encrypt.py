import rsa
import base64
from time import time


def rsaEncrypt(msg: str):
    """
    公钥加密
    :param msg: 要加密的内容
    :type msg: msg的加密内容必须是str类型
    :return: 加密之后的密文
    """
    """
    RSA加密:
    RSA是非对称加密，一般有：一对钥匙(公钥、私钥)
    客户端用公钥加密-->服务端用私钥解密)
    作为客户端: 要知道公钥(不同的项目都不一样)
    RSA加密显示的数据一般都是，sign形式的数据信息（只是sign数据信息都是被开发进行再次组装后显示出来的。）
    """
    # server_pub_key是每个项目不同的公钥字符串
    # -----BEGIN PUBLIC KEY-----这是公钥名称，必须用这个开头/结尾
    server_pub_key = """
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
    O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
    tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
    kKlZFc8Br7SHtbL2tQIDAQAB
    -----END PUBLIC KEY-----
    """

    # 生成公钥对象
    pub_key_byte = server_pub_key.encode("utf-8")
    # print(pub_key_byte)
    pub_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_byte)

    # 要加密的数据转成字节对象
    content = msg.encode("utf-8")

    # 加密,返回加密文本
    cryto_msg = rsa.encrypt(content, pub_key_obj)
    # base64编码
    cipher_base64 = base64.b64encode(cryto_msg)
    # 转成字符串
    return cipher_base64.decode()


# 返回RSA加密信息方法
# token的前50将位+当前时间作为加密信息，进行RAS加密然后返回加密信息sign，
# 时间戳timestamp是当前项目要求需要进行组装，才能请求有RSA的接口的
def generator_sign(token):
    # 获取token的前50位
    token_50 = token[:50]
    # 生成时间戳
    timestamp = int(time())
    # print(timestamp)
    # 接拼token前50位和时间戳
    msg = token_50 + str(timestamp)
    print(msg)
    # 进行RSA加密
    sign = rsaEncrypt(msg)
    return sign, timestamp


if __name__ == '__main__':
    import requests

    # lemon_v3测试
    headers = {"X-Lemonban-Media-Type": "lemonban.v3",
               "Content-Type": "application/json"}

    # 登陆接口
    login_url = "http://api.lemonban.com/futureloan/member/login"
    login_datas = {"mobile_phone": "15088314689", "pwd": "123456789"}
    resp = requests.request("POST", login_url, json=login_datas, headers=headers)
    resp = resp.json()
    token = resp["data"]["token_info"]["token"]
    member_id = resp["data"]["id"]

    headers["Authorization"] = "Bearer {}".format(token)
    sign, timestamp = generator_sign(token)
    print("签名为： ", sign, "\n时间戳为： ", timestamp)

    recharge_url = "http://api.lemonban.com/futureloan/member/recharge"
    recharge_data = {"member_id": member_id, "amount": 2000, "sign": sign, "timestamp": timestamp}
    resp = requests.request("POST", recharge_url, json=recharge_data, headers=headers)
    print(resp.json())
    # 充值接口
