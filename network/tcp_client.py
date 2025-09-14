import socket

target_host = "localhost"
target_port = 9998

# 创建socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 客户端连接服务器
client.connect((target_host, target_port))

# 发送数据
client.send("你好！服务器！".encode('utf-8'))

# 接收服务器返回的数据
response = client.recv(4096)

print(response.decode())
client.close()
