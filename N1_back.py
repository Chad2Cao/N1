import os
from pathlib import Path
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox

from pandas import DataFrame,read_csv,concat
from tkinter import Tk,Label,Button
import base64
from Crypto.Cipher import DES


global folder,program_folder
folder = Path(__file__).parent.resolve()
program_folder=folder.parent.parent.parent
def on_closing():
    # 在这里编写关闭窗口的代码
    root.destroy()


def select_csv_file():
    global input_path
    input_path = filedialog.askdirectory(title="选择输出文件目录", initialdir=os.path.join(program_folder,'csv'))
    input_label.config(text=input_path)


def select_output_path():
    global output_path
    output_path = filedialog.askdirectory(title="选择输出文件目录", initialdir=program_folder)
    output_label.config(text=output_path)


def create_folder():
    now = datetime.now()

    # 格式化时间
    time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    # 创建文件夹
    global out_folder_name
    out_folder_name = os.path.join(output_path, time_str)
    os.makedirs(out_folder_name)


def combine_csv(input_path):
    df = DataFrame()
    for filename in os.listdir(input_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_path, filename)
            data = read_csv(file_path, header=1, na_values=['NA'],
                               dtype={'TesterID': str, 'errCode': str, 'FIXTURE_ID': str})
            data.drop(range(0, 2), inplace=True)
            keep_columns = ['SerialNumber', 'overallResult', 'errCode', 'errString', 'stopTime', 'TesterID', 'testTime',
                            'SW_VER', 'CONFIG', 'TEST_SCRIPT', 'FIXTURE_ID', 'macOS', 'macMini', 'macRAM', 'PROJECT',
                            'COMP_VER', 'SpecVersion', 'MALIBU_FW_VERSION', 'BRIDGE_FW_VER', 'HERON_FW', 'DUT_FW_VER',
                            'CARRIER_PN', 'CARRIER_MAX_RUN', 'CARRIER_TOTAL_TEST', 'CARRIER_UNIT_FAIL',
                            'CARRIER_LOCK_STATUS']
            data = data[keep_columns]
            data['SerialNumber'] = data['SerialNumber'].str.split("+").str[0]
            # data['TesterID'] = data['TesterID'].astype(str)
            # data['FIXTURE_ID'] = data['FIXTURE_ID'].astype(str)
            df = concat([df, data], ignore_index=True)
    # df.to_csv(os.path.join(out_folder_name, "combine.csv"), index=False)
    return df


def get_input_count_of_tester(tester, df):
    return df[df['TesterID'] == tester]['SerialNumber'].nunique()


def get_fail_rate(df):
    # df.drop_duplicates(subset=['SerialNumber'], inplace=True)
    input = df['SerialNumber'].nunique()
    fail = df[df['overallResult'] == 'FAIL']['SerialNumber'].nunique()
    if input == 0:
        return 0, 0, 0
    rate = format((fail / input), '.2%')
    return input, fail, rate


def top_fail_testers(df, top):
    top_tester = df['TesterID'].value_counts().head(top).index.tolist()
    return top_tester


def top_fail_failures(df, top):
    top_failure = df['errString'].value_counts().head(top)
    return top_failure


def get_fail_rate_by_tester(tester, df):
    # df.drop_duplicates(subset=['SerialNumber'], inplace=True)
    df = df[df['TesterID'] == tester]
    return get_fail_rate(df)


def list_testers(df):
    # tester_series= df.loc['TesterID'].astype(str)
    return df['TesterID'].value_counts().index.tolist()


def get_fail_string(tester, df):
    df = df[df['TesterID'] == tester]
    fail_string = ''
    for index, value in top_fail_failures(df, 3).items():
        code = df[df['errString'] == index]['errCode'].tolist()[0]
        # print(df[df['errString']==index])
        fail_string += f"{code}_{index}:{value}R\n"
    return fail_string


def process_data():
    info_label.config(text="")
    if not input_path:
        info_label.config(text="注意：CSV文件夹未选择！")
        return
    if not output_path:
        info_label.config(text="注意：输出文件夹未选择！")
        return
    create_folder()
    df = combine_csv(input_path)
    input, fail, failrate = get_fail_rate(df)
    # print(input, fail, failrate)
    # top5_testers = top_fail_testers(df[df['overallResult'] == 'FAIL'], 5)
    list_fail_testers = list_testers(df[df['overallResult'] == 'FAIL'])
    tester_df = DataFrame(index=list_fail_testers, columns=['input', 'fail', 'failrate', 'fail_string'])
    for tester in list_fail_testers:
        input_, fail_, rate_ = get_fail_rate_by_tester(tester, df)
        fail_string_ = get_fail_string(tester, df[df['overallResult'] == 'FAIL'])
        tester_df.loc[tester] = [input_, fail_, rate_, fail_string_]
    # print(tester_df)
    sorter_df = tester_df.sort_values(by='failrate', ascending=False)
    sorter_df.to_csv(os.path.join(out_folder_name, "fail_tester.csv"), index=True)
    # csv_data=sorter_df.to_csv(index=True)
    # for row in csv_data.split('\n'):
    #     if row:
    #         table.insert('', 'end', values=row.split(','))
    info_label.config(text=f"TSP-E 整体复测率:{failrate} ({fail}R/{input}T)")


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)


def encrypt(text):
    padded_data = add_to_16(text)

    key = b"pro@chad"
    des = DES.new(key, DES.MODE_ECB)

    # 加密数据
    encrypted_data = des.encrypt(padded_data)

    # 将加密后的字节数组转换为十六进制字符串
    encrypted_hex = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_hex


def decrypt(encrypted_hex):
    key = b"pro@chad"
    # 创建DES对象，密钥必须是8字节长
    des = DES.new(key, DES.MODE_ECB)

    # 解密数据
    decrypted_data = des.decrypt(base64.b64decode(encrypted_hex))

    # 将解密后的字节数组转换为字符串
    decrypted_str = decrypted_data.decode('utf-8')
    return decrypted_str


def is_overdated():
    now = datetime.now()
    TRIAL_END_DATE = datetime(2024, 3, 1, 00, 00, 00)
    license_path = os.path.join(folder, "license.txt")
    if not os.path.exists(license_path):
        return True
    else:
        with open(license_path, "rb") as f:
            encrypted_data = f.read()
        # 解密数据
        decrypted_str = decrypt(encrypted_data)
        sep_count = decrypted_str.count("@@")
        if sep_count != 5:  # license error
            return True
        else:
            trial_end_str = decrypted_str.split("@@")[4]
            trial_end_date = datetime.strptime(trial_end_str, "%Y-%m-%d %H:%M:%S")
            if now > trial_end_date:  # 过期
                return True
            else:
                lldate_str = decrypted_str.split("@@")[1]
                lldate = datetime.strptime(lldate_str, "%Y-%m-%d %H:%M:%S")
                lastdate_str = decrypted_str.split("@@")[3]
                lastdate = datetime.strptime(lastdate_str, "%Y-%m-%d %H:%M:%S")
                if lldate > lastdate:  # lldate>lastdate
                    return True
                else:
                    lldate_str = lastdate_str
                    lastdate_str = now.strftime("%Y-%m-%d %H:%M:%S")
                    content = f"T%TRIAL_END_DATE%:@@{lldate_str}@@,this date=@@{lastdate_str}@@{trial_end_str}@@%TRIAL_END_DATE%T"
                    # print(content)
                    with open(license_path, "w") as f:
                        f.write(encrypt(content))
                    return False


root = Tk()
if is_overdated():
    root.withdraw()
    messagebox.showinfo("提示", "TSP-E 试用期已过！")
root.geometry("900x250+100+100")
root.title("Data analyzer")
input_label = Label(root, width=14, text="请选择CSV文件夹：")
input_label.grid(row=1, column=1, )
input_button = Button(root, text="请选择输入csv文件", command=select_csv_file)
input_button.grid(row=1, column=0, sticky='ew')
input_path = ""

output_label = Label(root, width=14, text="输出文件路径：")
output_label.grid(row=2, column=1, )
output_button = Button(root, text="请选择输出文件夹", command=select_output_path)
output_button.grid(row=2, column=0, sticky='ew')
output_path = ""

process_button = Button(root, text="处理数据", command=process_data)
process_button.grid(row=3, column=0, sticky='ew')

info_label = Label(root, text=" ")
info_label.grid(row=9, column=2)


# table = ttk.Treeview(root, columns=['input', 'fail', 'failrate'])
# table.grid(row=1, column=2, rowspan=8)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
