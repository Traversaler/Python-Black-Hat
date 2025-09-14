import socket

target_host = "127.0.0.1"
target_port = 9997

# 创建socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 发送数据(因为UDP是无连接协议，通信前不需要connect函数建立连接)
client.sendto(b"AAABBBCCC", (target_host, target_port))

# 接收数据
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()
