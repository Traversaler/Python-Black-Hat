import socket
import threading

IP = '0.0.0.0'
PORT = 9998


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 指定服务器监听的端口和IP
    server.bind((IP, PORT))
    # 开始监听，最大连接数设为5
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        # accept用于接受一个连接，将客户端socket对象保存到client变量、远程连接信息保存到address变量
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        # 创建新线程处理客户端连接，指定线程要执行handle_client函数，传入client变量将客户端socket对象传给处理函数
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')


if __name__ == '__main__':
    main()
