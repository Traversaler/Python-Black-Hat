import paramiko


def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    # 用密钥认证代替密码认证，真实环境使用SSH密钥认证
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())


if __name__ == '__main__':
    # getpass库可以获取当前登录用户的用户名
    import getpass
    # user = getpass.getuser()
    # 服务器和设备用户名不同，所以仍旧需要输入
    user = input('Username:')
    # 用户输入密码，敲击字符不会出现在屏幕上
    password = getpass.getpass()
    ip = input('Enter server IP: ')
    port = input('Enter port or <CR>: ')
    cmd = input('Enter command or <CR>: ')
    ssh_command(ip, port, user, password, cmd)

