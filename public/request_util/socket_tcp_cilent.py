# tcp/udp请求流：服务端先运行，客户端再运行。
# 客户端发起tcp请求
from socket import *

# 填写本地主机地址/本地ipv4主机地址
host = gethostname()  # DESKTOP-AAE2JII
# ipv4地址获取：通过cmd命令:ipconfig，找到IPV4地址，例:163.0.3.2

# 填写服务端接口的端口号（测试tcp接口时，找sever要）
port = 1300

# 1,创建tcp的套接字
clientScoket = socket(family=AF_INET, type=SOCK_STREAM)

# 使用套接字
# 2,建立服务端severSocket连接（必须通过元组的方式，进行传参！）
# clientScoket.connect((host, port))
clientScoket.connect(("192.168.31.123", port))

# 填写请求参数信息
message = input("请输入请求参数信息:\n ")

# 3,在已连接的socket上发送数据【send()发送数据必须是but类型！】
clientScoket.send(message.encode("gbk"))

# 4,接收响应数据,【如果进行接收响应数据，那么必须接收到数据后才会停止socket运行，否则会一直运行socket等待接收响应数据为止】
# 设置接收响应数据的内存大小，并转换为str类型
upperMessage = clientScoket.recv(1024 * 10).decode("gbk")
print(f"接收服务端返回数据为：\n{upperMessage}")

# 5,不用的时候，关闭套接字（释放资源）
clientScoket.close()

if __name__ == '__main__':
    pass
