import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    # 去除命令开头和结尾的空格、换行字符
    cmd = cmd.strip()
    # 检查cmd是否为空，为空直接返回
    if not cmd:
        return
    # subprocess库提供了一组进程创建接口，可以通过多种方式调用其他程序。check_output函数会在本机运行一条命令并返回输出
    # split把命令拆分成程序能理解的格式，stderr是把错误信息也包含在输出中
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

    return output.decode()


class NetCat:
    # 类的方法（构造函数），self是对象自身的引用
    def __init__(self, args, buffer=None):
        # 将传入参数保存为对象的属性，供其他方法使用
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置套接字选项，SO_REUSEADDR允许地址重用，服务器重启后能使用相同端口
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 通过self可以在方法内部访问对象属性self.args，调用对象的方法listen
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        # 无限循环使服务器持续运行接受新的客户端连接
        while True:
            # 接受新的socket对象，_是忽略返回的客户端地址信息
            client_socket, _ = self.socket.accept()
            # 创建新线程处理客户端连接，将已连接的socket对象传给handle函数
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            # 将命令执行结果发回客户端
            client_socket.send(output.encode())

        elif self.args.upload:
            # 创建空的缓冲区，存储接收的数据
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    # 持续接收命令输入，换行符表示结束
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


if __name__ == '__main__':
    # parser对象实例，argparse模块，ArgumentParser类。创建一个命令行参数解析器
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # 帮助信息，给出示例。textwrap.dedent可以去除多行字符串每行前面的共同缩进
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
            ''')
    )
    # 调用方法add_argument
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    # 解析命令行参数，返回包含所有命令行参数值的对象
    args = parser.parse_args()
    '''
    程序在监听就把空白缓冲区传给NetCat对象，反之把stdin标准输入里数据传过去
    服务器在监听，启动时并没有主动要发送的数据，所以缓冲区为空来等待接收的数据
    客户端连接服务器去发送数据，stdin就是获取输入的数据
    '''
    if args.listen:
        buffer = ''
    else:
        # sys是模块，stdin是sys模块中一个对象，read是一个方法
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()
