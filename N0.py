import threading

import csv
import os
import shutil
import tkinter
from pathlib import Path
from tkinter import Tk, Label, Button, Entry, Radiobutton, StringVar, Text, BooleanVar, Checkbutton, Frame,messagebox
import paramiko
from datetime import datetime, timedelta

from ping3 import ping

# 目标Mac电脑的IP地址、用户名和密码
ip_list = []

username = 'gdlocal'
password = 'gdlocal'
# username = 'chad'
# password = 'Abcd.6666'

# 指定要从Mac上复制的csv文件路径和要保存到本地的路径
remote_proj_path = '/vault/D951_MP'
# remote_proj_path = '/Users/chad/Desktop/remote'
remote_path = ''
global folder, program_folder
folder = Path(__file__).parent.resolve()
program_folder = folder.parent.parent.parent
ip_path_tsp = os.path.join(folder, "ip_tsp.txt")
ip_path_dva = os.path.join(folder, "ip_dva.txt")
ip_path_mp9 = os.path.join(folder, "ip_mp9.txt")
# ip_path_tsp = os.path.join(folder, "ip.txt")
# ip_path_dva = os.path.join(folder, "ip.txt")
# ip_path_mp9 = os.path.join(folder, "ip.txt")
local_dir_path = os.path.join(program_folder, 'csv')  # change folder to program_folder when package


def replace_remote_path(path_str):
    remote_file.delete(0, tkinter.END)
    remote_file.insert(0, path_str)


def on_radiobutton_selected():
    select_station = var0.get()
    if select_station == 'TSP':
        replace_remote_path('/vault/D951_MP')
    elif select_station == 'DVA':
        replace_remote_path('/vault/Atlas')
    elif select_station == 'MP9':
        replace_remote_path('/vault/DMX/summary')


# def get_date():
#     selected = var1.get()
#
#     if selected == '昨天':
#         select_date = datetime.now() - timedelta(days=1)
#     elif selected == '前天':
#         select_date = datetime.now() - timedelta(days=2)
#     elif selected == '一周':
#         start_date = datetime.now() - timedelta(days=7)
#         end_date = datetime.now()
#         date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]
#         str_list = [date.strftime('%Y%m%d') for date in date_list]
#         str_join = ','.join(str_list)
#         format_str = '{' + str_join + '}'
#
#         return format_str
#     else:
#         select_date = datetime.now()
#     return select_date.strftime('%Y%m%d')


# def get_tsp_date():
#     # global select_date
#     selected = var1.get()
#
#     if selected == '昨天':
#         select_date = datetime.now() - timedelta(days=1)
#     elif selected == '前天':
#         select_date = datetime.now() - timedelta(days=2)
#     elif selected == '一周':
#         start_date = datetime.now() - timedelta(days=7)
#         end_date = datetime.now()
#         date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]
#         str_list = [date.strftime('%Y-%m-%d') for date in date_list]
#         str_join = ','.join(str_list)
#         format_str = '{' + str_join + '}'
#
#         return format_str
#
#     else:
#         select_date = datetime.now()
#     return select_date.strftime('%Y_%m_%d')
#     # print(remote_dir_path)


def insert_text(local_):
    local_file.config(state='normal', bg='#303030', fg='white')
    local_file.insert(tkinter.END, local_ + '\n')
    local_file.config(state='disabled', bg='#303030', fg='white')


def process_Macs():
    if check_var.get():
        process_Macs_from_file()
    else:
        Process_Mac_from_ip()


def Process_Mac_from_ip():
    ip = remote_ip.get()
    username = username_entry.get()
    password = password_entry.get()
    proj_path = remote_file.get()
    remote_path = proj_path
    if not is_network_alive(ip):
        info_label.config(text=f"{ip} network is not alive！")
        return
    else:
        for date_comp in get_date_list():
            copy_files_from_mac(ip, username, password, remote_path, date_comp)
        rename_mp9_files()


def isMP9log(filename):
    if filename.endswith('MP9.2_summary.csv'):
        return True
    else:
        return False


def get_stationID_from_file(file_):
    with open(file_, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        next(reader)
        next(reader)
        for line in reader:
            return line[5]


def rename_mp9_files():
    for file in os.listdir(local_dir_path):
        if isMP9log(file) and not file.startswith('LYSX_A01-3FT-'):
            file_path = os.path.join(local_dir_path, file)
            file_name = os.path.basename(file_path)
            new_filename = get_stationID_from_file(file_path) + '_' + file_name
            new_file_path = os.path.join(local_dir_path, new_filename)
            os.rename(file_path, new_file_path)


def get_date_list():
    selected = var1.get()
    if selected == '昨天':
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now()
    elif selected == '前天':
        start_date = datetime.now() - timedelta(days=2)
        end_date = datetime.now() - timedelta(days=1)
    elif selected == '一周':
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
    else:
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=1)

    date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]
    combined_str_list = [[date.strftime('%Y_%m_%d'), date.strftime('%Y%m%d')] for date in date_list]
    return combined_str_list


def process_Macs_from_file():
    ip_path = ''
    if var0.get() == 'TSP':
        ip_path = ip_path_tsp
    elif var0.get() == 'DVA':
        ip_path = ip_path_dva
    elif var0.get() == 'MP9':
        ip_path = ip_path_mp9
    if not os.path.exists(ip_path):
        info_label.config(text="ip file not exist!")
        return
    else:
        with open(ip_path, 'r') as f:
            ips = f.readlines()
        if not os.path.exists(local_dir_path):
            os.makedirs(local_dir_path)
        for ip in ips:
            ip = ip.strip()  # 去除换行符和空格
            if not is_network_alive(ip):
                info_label.config(text=f"{ip} network is not alive！")
                insert_text(f'{ip} is not alive!')
                continue
            else:
                username = username_entry.get()
                password = password_entry.get()
                proj_path = remote_file.get()
                remote_path = proj_path
                for date_comp in get_date_list():
                    copy_files_from_mac(ip, username, password, remote_path, date_comp)
                rename_mp9_files()


def copy_files_from_mac(ip, username_, password_, remote_path_, date_comp_):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username_, password=password_)
    except Exception as e:
        info_label.config(text=f"connect {ip} failed for:{e}")
        insert_text(f'connect {ip} failed for:{e})')
        ssh.close()
        return
    info_label.config(text=f"connect {ip} success!")

    if var0.get() == 'TSP':
        remote_path_ = os.path.join(remote_path_, date_comp_[0])
        stdin, stdout, stderr = ssh.exec_command(f'ls {remote_path_}/TSP_*.csv')
    elif var0.get() == 'DVA':
        stdin, stdout, stderr = ssh.exec_command(f'ls {remote_path_}/Summary_*{date_comp_[1]}.csv')
    elif var0.get() == 'MP9':
        stdin, stdout, stderr = ssh.exec_command(f'ls {remote_path_}/{date_comp_[1]}_*summary.csv')
    csv_files = stdout.read().decode().split('\n')
    if csv_files == ['']:
        info_label.config(text=f"no correct csv file under {remote_path_}")
        insert_text(f"no correct csv file under {remote_path_}")
        ssh.close()
        return
    if not os.path.exists(local_dir_path):
        os.makedirs(local_dir_path)
    for file in csv_files:
        # print(file)
        if file.endswith('.csv'):
            file = os.path.basename(file)
            # print(file)
            remote_file_name = os.path.join(remote_path_, file)
            # print(remote_file_name)
            local_file_name = os.path.join(local_dir_path, file)
            sftp = ssh.open_sftp()
            sftp.get(remote_file_name, local_file_name)
            sftp.close()
            # info_label.config(text=f"{local_file}")
            insert_text(f"--->{local_file_name}")
    # print(stdout.read().decode())
    ssh.close()


def clear_local_csv():
    folder_path = local_dir_path
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            info_label.config(text=f"delete {file_path}failed！for: {e}")
    local_file.config(state='normal', bg='#303030', fg='white')
    local_file.delete(1.0, tkinter.END)
    local_file.config(state='disabled', bg='#303030', fg='white')


def is_network_alive(ip):
    try:
        delay = ping(ip)  # 单位为毫秒
        if delay is not None:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def start_thread():
    t = threading.Thread(target=process_Macs)
    t.start()


root = Tk()

root.geometry("1050x300+250+200")
root.title("Data Getter")
# remote_IP_label = Label(root, text="IP", width=15)
# remote_IP_label.grid(row=0, column=0)
# username_label = Label(root, text="Username", width=15)
# username_label.grid(row=0, column=1)
#
# password_label = Label(root, text="password", width=15)
# password_label.grid(row=0, column=2)
# remote_path_label = Label(root, text="remote path", width=15)
# remote_path_label.grid(row=0, column=3)
var0 = StringVar()
radio1 = Radiobutton(root, text='TSP', value='TSP', variable=var0, command=on_radiobutton_selected)
radio1.grid(row=0, column=0)
radio2 = Radiobutton(root, text='DVA', value='DVA', variable=var0, command=on_radiobutton_selected)
radio2.grid(row=0, column=1)
radio3 = Radiobutton(root, text='MP9', value='MP9', variable=var0, command=on_radiobutton_selected)
radio3.grid(row=0, column=2)
var0.set('TSP')

remote_ip = Entry(root, width=12)
remote_ip.grid(row=1, column=0, sticky='w')
remote_ip.insert(0, '127.0.0.1')

username_entry = Entry(root, width=12)
username_entry.grid(row=1, column=1, sticky='w')
username_entry.insert(0, username)

password_entry = Entry(root, width=12)
password_entry.grid(row=1, column=2, sticky='w')
password_entry.insert(0, password)

remote_file = Entry(root, width=15)
remote_file.grid(row=1, column=3)
remote_file.insert(0, remote_proj_path)

check_var = BooleanVar()
check_button = Checkbutton(root, text="IPS", variable=check_var)
check_button.grid(row=1, column=4, sticky='w')

# remote_file_label = Label(root, text="remote file")
# remote_file_label.grid(row=2, column=0)


var1 = StringVar()
radio1 = Radiobutton(root, text='yesterday', value='昨天', variable=var1)
radio1.grid(row=1, column=6)
radio2 = Radiobutton(root, text='today', value='今天', variable=var1)
radio2.grid(row=1, column=5)
radio3 = Radiobutton(root, text='3day before', value='前天', variable=var1)
radio3.grid(row=1, column=7)
radio4 = Radiobutton(root, text='OneWeek', value='一周', variable=var1)
radio4.grid(row=1, column=8)
var1.set('今天')
local_file = Text(root, width=115, height=15)
local_file.config(state='disabled', bg='#303030', fg='white')
local_file.grid(row=2, column=0, columnspan=7)

info_label = Label(root, text="...", width=90)
info_label.grid(row=3, column=0, columnspan=7, sticky='w')

left_frame = Frame(root, width=100)
left_frame.grid(row=2, column=7, columnspan=2)

open_button = Button(left_frame, text="OneKeyCopy", width=12, command=start_thread)
open_button.grid(row=0, column=0, sticky='n')

clear_button = Button(left_frame, text="clear local CSV files", width=12, command=clear_local_csv)
clear_button.grid(row=2, column=0)

root.mainloop()
