import os, stat
from pathlib import Path

import paramiko
from tkinter import Tk ,Label, Button


# 定义一个递归函数来遍历远程目录及其子目录
def recursive_copy_csv(sftp, remote_base, local_base):
    for entry in sftp.listdir_attr(remote_base):
        remote_path = os.path.join(remote_base, entry.filename)
        local_path = os.path.join(local_base, entry.filename)

        if stat.S_ISDIR(entry.st_mode):  # 如果是目录，则递归进入
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            recursive_copy_csv(sftp, remote_path, local_path)
        elif entry.filename.endswith('.csv'):  # 如果是.csv文件，则进行复制
            sftp.get(remote_path, local_path)
            print(f"File {entry.filename} has been copied from Mac to local.")

# 目标Mac电脑的IP地址、用户名和密码
ip_list = []


username = 'gdlocal'
password = 'gdlocal'  # 如果使用密钥对认证则不需要此变量

# 指定要从Mac上复制的csv文件路径和要保存到本地的路径
remote_dir_path = ''
local_dir_path = ''
folder = Path(__file__).parent.resolve()
ip_path = os.path.join(folder, "ip.txt")
location_path = os.path.join(folder, "location.txt")

if os.path.exists(ip_path):
    # 打开并读取location.txt文件
    with open(ip_path, 'r') as file:
        ip_list = file.readlines()


if os.path.exists(location_path):
    # 打开并读取location.txt文件
    with open(location_path, 'r') as file:
        lines = file.readlines()

    # 初始化一个空字典来存储键值对
    data_dict = {}

    # 遍历文件的每一行
    for line in lines:
        # 去除末尾换行符并使用'='进行分割
        line = line.replace(" ", "")
        line = line.replace("'", "")
        key, value = line.split('=')


    # 将分割后的两部分存入字典中
        data_dict[key] = value
    # 输出处理后的字典
    remote_file_path = data_dict['remote_dir_path']
    local_dir_path = data_dict['local_dir_path']
    # print(remote_file_path, local_dir_path)

def copy_file():

    # 确保本地目录存在
    if not os.path.exists(local_dir_path):
        os.makedirs(local_dir_path)

    # 创建一个SSH客户端对象
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机密钥到本地缓存

    # 连接到Mac电脑
    for mac_ip in ip_list:
        ssh.connect(mac_ip, username=username, password=password)

        # 打开SFTP会话
        sftp_client = ssh.open_sftp()


        # 调用递归函数开始复制过程
        recursive_copy_csv(sftp_client, remote_dir_path, local_dir_path)

    # 关闭SFTP会话和SSH连接
    sftp_client.close()
    ssh.close()

# print("All CSV files have been successfully copied.")
root = Tk()

root.geometry("300x100+550+200")
root.title("Data Getter")

info_label = Label(root, text="copy the file on tester")
info_label.grid(row=0, column=0)

open_button = Button(root, text="copy", command=copy_file)
open_button.grid(row=0, column=1)

root.mainloop()