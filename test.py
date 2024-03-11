import paramiko
import os

# 读取ip.txt文件中的IP地址
with open('ip.txt', 'r') as f:
    ips = f.readlines()

# 遍历每个IP地址，建立SSH连接并复制文件
for ip in ips:
    ip = ip.strip()  # 去除换行符和空格
    print(ip)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机密钥
    ssh.connect(ip, username='chad', password='Abcd.6666')  # 替换为你的用户名和密码
    # 在远程服务器上列出所有以.csv结尾的文件
    stdin, stdout, stderr = ssh.exec_command('ls /Users/te/Desktop/123/2024_02_07/*.csv')
    print(stdout.read().decode())

    # 执行命令获取MAC地址
    # stdin, stdout, stderr = ssh.exec_command('ifconfig | grep "ether" | awk \'{print $2}\'')
    # mac = stdout.read().decode().strip()

    # 构造本地目录路径和远程目录路径
    # local_dir = '/Users/chad/Desktop/csv'
    # remote_dir = '/vault/MP_D951/2024_02_05'
    #
    # # 遍历远程目录下的CSV文件，并复制到本地目录
    # for file in os.listdir(remote_dir):
    #     if file.endswith('.csv'):
    #         remote_file = os.path.join(remote_dir, file)
    #         local_file = os.path.join(local_dir, file)
    #         sftp = ssh.open_sftp()
    #         sftp.get(remote_file, local_file)
    #         sftp.close()
    #
    # ssh.close() # 关闭SSH连接

from ping3 import ping


def is_network_alive(ip):
    try:
        delay = ping(ip)  # 单位为毫秒
        if delay is not None:
            return True
        else:
            return False
    except  Exception as e:
        return False


ip = "8.8.8.8"  # 你可以替换为任意IP地址
if is_network_alive(ip):
    print("网络通畅")
else:
    print("网络不通")

import os
import shutil


def delete_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


folder_path = '你的文件夹路径'
delete_all_files_in_folder(folder_path)

# c = 123

