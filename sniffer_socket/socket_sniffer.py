import socket
import os

# Windows管理员权限下才能启用网卡的混杂模式运行
# host to listen on
HOST = '192.168.133.79'


def main():
    # 创建socket
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    # 抓包时包含IP头
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Windows网卡混杂模式，接收所有经过网卡的数据包（不仅是发给本机的）
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    # 读一个包
    print(sniffer.recvfrom(65565))
    # 关闭混杂模式
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()

