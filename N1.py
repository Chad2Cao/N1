import threading
import sys
import warnings
import csv
import os
from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox
from pandas import DataFrame, read_csv, concat, isnull, to_datetime
from tkinter import Tk, Label, Button, Radiobutton, Frame, StringVar, Text
import base64
from Crypto.Cipher import DES

global folder, program_folder
folder = Path(__file__).parent.resolve()
# messagebox.showinfo("info",str(folder))
# file_str = sys.argv[0]  #/Users/chad/Desktop/N1.app/Contents/MacOS/N1

# messagebox.showinfo("info",str(folder))


# folder_str = file_str.split('/N1.app')[0]
# folder =Path(folder_str)
folder = folder.parent.parent.parent  # change to this when package
# messagebox.showinfo("info",str(folder))
# 忽略警告
warnings.filterwarnings('ignore')
def on_closing():
    # 在这里编写关闭窗口的代码
    root.destroy()


def select_csv_file():
    global input_path
    input_path = filedialog.askdirectory(title="please select the input folder", initialdir=os.path.join(folder, 'csv'))
    input_label.config(text=input_path)


def select_output_path():
    global output_path
    output_path = filedialog.askdirectory(title="please select output folder", initialdir=folder)
    output_label.config(text=output_path)


def create_folder():
    now = datetime.now()

    # 格式化时间
    time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    # 创建文件夹
    global out_folder_name
    out_folder_name = os.path.join(output_path, time_str)
    os.makedirs(out_folder_name)


def tsp_Probe_key_list():
    probe_key_list = []
    file_path = os.path.join(Path(__file__).parent.resolve(), 'key_for_probe.csv')
    # info_label.config(text=f" get {file_path} ")
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        # 创建csv阅读器对象
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        # 遍历csv文件的每一行
        for row in csv_reader:
            key_dict = {'key': row[0], 'spec': row[1], 'probe': row[2]}
            probe_key_list.append(key_dict)
    return probe_key_list


def Spec_key_list():
    spec_key_list = []
    file_path = os.path.join(Path(__file__).parent.resolve(), 'key_for_spec.csv')
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        # 创建csv阅读器对象
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        # 遍历csv文件的每一行
        for row in csv_reader:
            key_dict = {'key': row[0], 'spec': row[1]}
            spec_key_list.append(key_dict)
    return spec_key_list


def isTSPlog(filename_):
    if filename_.startswith('TSP_') and filename_.endswith('.csv'):
        return True
    else:
        return False


def combine_tsp_csv(input_path):
    df = DataFrame()
    for filename in os.listdir(input_path):
        if isTSPlog(filename):
            file_path = os.path.join(input_path, filename)
            # info_label.config(text=f"文件:{filename} start combine")
            insert_text('combining：' + filename)
            ori_data = read_csv(file_path, header=1, na_values=['NA'],
                                dtype={'FIRST_FAILED_SPEC': str, 'TesterID': str, 'errCode': str, 'FIXTURE_ID': str})
            ori_data.drop(range(0, 2), inplace=True)
            keep_columns = ['SerialNumber', 'overallResult', 'errCode', 'errString', 'FIRST_FAILED_SPEC', 'startTime',
                            'stopTime', 'TesterID', 'testTime',
                            'SW_VER', 'CONFIG', 'TEST_SCRIPT', 'FIXTURE_ID', 'macOS', 'macMini', 'macRAM', 'PROJECT',
                            'COMP_VER', 'SpecVersion', 'MALIBU_FW_VERSION', 'BRIDGE_FW_VER', 'HERON_FW', 'DUT_FW_VER',
                            'CARRIER_PN', 'CARRIER_MAX_RUN', 'CARRIER_TOTAL_TEST', 'CARRIER_UNIT_FAIL',
                            'CARRIER_LOCK_STATUS']
            data = ori_data[keep_columns]
            data = data.dropna(subset=['SerialNumber'])  # Return a new Series with missing values removed.
            data.loc[:, 'first_failed_value'] = ""
            data.loc[:, 'first_failed_spec'] = ""
            data.loc[:, 'first_failed_probe'] = ""

            for index, row in ori_data.iterrows():
                if row['overallResult'] == 'FAIL':
                    key = row['FIRST_FAILED_SPEC']
                    try:

                        value = row[key]
                    except KeyError:
                        # 处理除以0的情况
                        value = "NA"
                    except Exception as e:
                        # 处理其他未知异常
                        print("error：", str(e))
                    data.loc[index, 'first_failed_value'] = value
                    # spec_list = Spec_key_list()
                    # for d in spec_list:
                    #     if key == d['key']:
                    #         data.loc[index, 'first_failed_spec'] = d['spec']
                    probe_key_list = tsp_Probe_key_list()
                    for d in probe_key_list:
                        if key == d['key']:
                            data.loc[index, 'first_failed_probe'] = d['probe']
                            data.loc[index, 'first_failed_spec'] = d['spec']

            data['SerialNumber'] = data['SerialNumber'].str.split("+").str[0]
            data.rename(columns={'startTime': 'StartTime'}, inplace=True)
            df = concat([df, data], ignore_index=True)

    df.to_csv(os.path.join(out_folder_name, "combine.csv"), index=False)
    return df


def get_from_filename(filename: str):
    tester_id = filename.split('_')[3]
    return f'DVA-{tester_id}'


def isDVAlog(filename_):
    if filename_.endswith('.csv') and filename_.startswith('Summary_') and 'IQC-DISPLAY-3' in filename_:
        return True
    else:
        return False


def combine_dva_csv(input_path):
    df = DataFrame()
    for filename in os.listdir(input_path):
        if isDVAlog(filename):
            file_path = os.path.join(input_path, filename)
            insert_text('combining：' + filename)
            ori_data = read_csv(file_path, header=0, na_values=['NA'], dtype={'FIXTURE_ID': str, 'FailedTestName': str,
                                                                              'FailedValue': float, 'FailedUL': str,
                                                                              'FailedLL': str, 'Fail Type': str})
            # ori_data.drop(range(0, 2), inplace=True)
            keep_columns = ['SerialNumber', 'StartTime', 'FailedTestName', 'FailedValue', 'FailedUL', 'FailedLL',
                            'Fail Type', 'Head Id', 'cameraSN', 'carrierSN', 'softwareversion']
            data = ori_data[keep_columns]
            data = data.dropna(subset=['SerialNumber'])  # Return a new Series with missing values removed.
            data.rename(columns={'FailedTestName': 'errString'}, inplace=True)
            data.rename(columns={'carrierSN': 'CARRIER_PN'}, inplace=True)

            data.loc[:, 'TesterID'] = get_from_filename(filename)
            # data.loc[:, 'overallResult'] ='PASS'
            # data[data['errString'].isnull()]['overallResult']='FAIL'
            # for index, row in data.iterrows():
            #     data.loc[index, 'overallResult'] = np.where(data.loc[index,'errString'].isnull(), 'PASS', 'FAIL')
            data['overallResult'] = data.apply(lambda row: 'PASS' if isnull(row['errString']) else 'FAIL', axis=1)
            df = concat([df, data], ignore_index=True)
    # df.to_csv(os.path.join(out_folder_name, "dva_combine.csv"), index=False)
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


def top_first_fail_spec(df, top):
    top_failure = df['FIRST_FAILED_SPEC'].value_counts().head(top)
    return top_failure


def get_fail_rate_by_tester(tester, df):
    # df.drop_duplicates(subset=['SerialNumber'], inplace=True)
    df = df[df['TesterID'] == tester]
    return get_fail_rate(df)


def list_testers(df):
    # tester_series= df.loc['TesterID'].astype(str)
    return df['TesterID'].value_counts().index.tolist()


def get_tsp_fail_string(tester, df):
    df = df[df['TesterID'] == tester]
    fail_string = ''
    spec_detail = ''
    for index, value in top_fail_failures(df, 5).items():
        code = df[df['errString'] == index]['errCode'].tolist()[0]

        # print(df[df['errString']==index])
        fail_string += f"{code}_{index}:{value}R\n"
    for index, value in top_first_fail_spec(df, 5).items():
        if index in [d['key'] for d in tsp_Probe_key_list()]:
            probe = df[df['FIRST_FAILED_SPEC'] == index]['first_failed_probe'].tolist()[0]
            failed_value = df[df['FIRST_FAILED_SPEC'] == index]['first_failed_value'].tolist()
            failed_value_round = tuple([round(x, 2) for x in failed_value])
            spec = df[df['FIRST_FAILED_SPEC'] == index]['first_failed_spec'].tolist()[0]
            # print(df[df['errString']==index])
            spec_detail += f"{index}:{value}R -->value:{failed_value_round}{spec}@{probe}\n"
    return fail_string, spec_detail


def get_dva_fail_string(tester, df):
    df = df[df['TesterID'] == tester]
    fail_string = ''
    fail_detail = ''
    for index, value in top_fail_failures(df, 5).items():
        failed_value = df[df['errString'] == index]['FailedValue'].tolist()
        failed_value_round = tuple([round(x, 2) for x in failed_value])
        UL = df[df['errString'] == index]['FailedUL'].tolist()[0]
        LL = df[df['errString'] == index]['FailedLL'].tolist()[0]
        # print(df[df['errString']==index])
        fail_string += f"{index}:{value}R\n"
        fail_detail += f"{index}:{failed_value_round}[{LL}~{UL}]\n"

    return fail_string, fail_detail


def get_mp9_fail_string(tester, df):
    df = df[df['TesterID'] == tester]
    fail_string = ''
    spec_detail = ''
    for index, value in top_fail_failures(df, 5).items():
        fail_string += f"{index}:{value}R\n"
        if index in [d['key'] for d in mp9_key_list()]:
            failed_value = df[df['errString'] == index]['first_failed_value'].tolist()
            failed_list = [float(x) for x in failed_value]
            failed_value_round = tuple([round(x, 2) for x in failed_list])
            spec = df[df['errString'] == index]['first_failed_spec'].tolist()[0]
            spec_detail += f"{index}-->value:{failed_value_round}{spec}\n"

    return fail_string, spec_detail


def get_time_range(df):
    df['StartTime'] = to_datetime(df['StartTime'])
    df = df.sort_values('StartTime')
    start = df['StartTime'].head(1).values[0].astype(str).split('.')[0].replace('T',' ')
    end = df['StartTime'].tail(1).values[0].astype(str).split('.')[0].replace('T',' ')
    return start, end


def process_tsp_data():
    df = combine_tsp_csv(input_path)
    start, end = get_time_range(df)
    input, fail, failrate = get_fail_rate(df)
    # print(input, fail, failrate)
    # top5_testers = top_fail_testers(df[df['overallResult'] == 'FAIL'], 5)
    list_fail_testers = list_testers(df[df['overallResult'] == 'FAIL'])
    tester_df = DataFrame(index=list_fail_testers, columns=['input', 'fail', 'failrate', 'fail_string', 'fail_detail'])
    # info_label.config(text=f"process tsp data:")
    for tester in list_fail_testers:
        input_, fail_, rate_ = get_fail_rate_by_tester(tester, df)
        fail_string_, spec_detail_ = get_tsp_fail_string(tester, df[df['overallResult'] == 'FAIL'])
        tester_df.loc[tester] = [input_, fail_, rate_, fail_string_, spec_detail_]
    # print(tester_df)
    tester_df['failrate'] = tester_df['failrate'].str.rstrip('%').astype(float)
    sorter_df = tester_df.sort_values(by='failrate', ascending=False)
    sorter_df['failrate'] = sorter_df['failrate'].astype(str) + '%'
    sorter_df.to_csv(os.path.join(out_folder_name, "fail_tester_TSP.csv"), index=True)
    info_label.config(text=f"time range:[{start}~{end}], TSP-E overall retest:{failrate} ({fail}R/{input}T)")


def process_dva_data():
    df = combine_dva_csv(input_path)
    start, end = get_time_range(df)
    input, fail, failrate = get_fail_rate(df)
    # print(input, fail, failrate)
    # top5_testers = top_fail_testers(df[df['overallResult'] == 'FAIL'], 5)
    list_fail_testers = list_testers(df[df['overallResult'] == 'FAIL'])
    tester_df = DataFrame(index=list_fail_testers, columns=['input', 'fail', 'failrate', 'fail_string', 'probe_detail'])
    for tester in list_fail_testers:
        input_, fail_, rate_ = get_fail_rate_by_tester(tester, df)
        fail_string_, spec_detail_ = get_dva_fail_string(tester, df[df['overallResult'] == 'FAIL'])
        tester_df.loc[tester] = [input_, fail_, rate_, fail_string_, spec_detail_]
    # print(tester_df)
    tester_df['failrate'] = tester_df['failrate'].str.rstrip('%').astype(float)
    sorter_df = tester_df.sort_values(by='failrate', ascending=False)
    sorter_df['failrate'] = sorter_df['failrate'].astype(str) + '%'
    sorter_df.to_csv(os.path.join(out_folder_name, "fail_tester_DVA.csv"), index=True)
    info_label.config(text=f"time range:[{start}~{end}],DVA overall retest :{failrate} ({fail}R/{input}T)")


def isMP9log(filename):
    if filename.endswith('MP9.2_summary.csv'):
        return True
    else:
        return False


def get_overallResult(row):
    if (row['MP9 DMX1_Result'] == 'binA' and row['MP9 DMX2_Result'] == 'binA' and row['MP9 UNLD_Result'] == 'OK'
            and row['MP9 Binning'] == 'binA'):
        return 'PASS'
    else:
        return 'FAIL'


def mp9_key_list():
    key_spec_list = []
    file_path = os.path.join(Path(__file__).parent.resolve(), 'mp9_key_spec.csv')
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        # 创建csv阅读器对象
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        # 遍历csv文件的每一行
        for row in csv_reader:
            key_dict = {'key': row[0], 'spec': f'[{row[1]}~{row[2]}]'}
            key_spec_list.append(key_dict)
    return key_spec_list


def combine_mp9_csv(input_path):
    df = DataFrame()
    for filename in os.listdir(input_path):
        if isMP9log(filename):
            file_path = os.path.join(input_path, filename)
            insert_text('combining：' + filename)
            ori_data = read_csv(file_path, header=0, na_values=['NA'],
                                dtype={'FIRST_FAILED_SPEC': str, 'TesterID': str, 'errCode': str,
                                       'FIXTURE_ID': str})
            ori_data.drop(range(0, 2), inplace=True)
            keep_columns = ['serialnumber', 'StartTime', 'StopTime', 'Test Time', 'StationID', 'NEST_ID',
                            'MP9 PM_Result', 'MP9 UNLD_Result', 'MP9 Test Pass/Fail', 'List_of_Failing_Items',
                            'MP9 DMX1_Result', 'MP9 DMX2_Result', 'MP9 Binning',
                            'softwareversion', 'MP9_CARRIER_SN']
            data = ori_data[keep_columns]
            data.loc[:, 'first_failed_key'] = ""
            data.loc[:, 'first_failed_value'] = ""
            data.loc[:, 'first_failed_spec'] = ""
            data['overallResult'] = data.apply(get_overallResult, axis=1)

            for index, row in ori_data.iterrows():
                if data.loc[index, 'overallResult'] == 'FAIL':
                    key = row['List_of_Failing_Items'].split(';')[0]
                    key = key.replace(' CoF', '')
                    try:
                        value = row[key]
                    except KeyError:
                        # 处理除以0的情况
                        value = "NA"
                    except Exception as e:
                        # 处理其他未知异常
                        print("发生错误：", str(e))
                    data.loc[index, 'first_failed_key'] = key
                    data.loc[index, 'first_failed_value'] = value
                    spec_list = mp9_key_list()
                    for d in spec_list:
                        if key == d['key']:
                            data.loc[index, 'first_failed_spec'] = d['spec']
            data.rename(columns={'serialnumber': 'SerialNumber'}, inplace=True)
            data.rename(columns={'StationID': 'TesterID'}, inplace=True)
            data.rename(columns={'MP9_CARRIER_SN': 'CARRIER_PN'}, inplace=True)
            data.rename(columns={'first_failed_key': 'errString'}, inplace=True)
            data = data.dropna(subset=['SerialNumber', 'MP9 PM_Result', 'MP9 DMX1_Result', 'MP9 DMX2_Result'])
            data['CARRIER_PN'] = data['CARRIER_PN'].apply(lambda x: '294100' + hex(int(x))[2:].upper())

            df = concat([df, data], ignore_index=True)
    # df.to_csv(os.path.join(out_folder_name, "mp9_combine.csv"), index=False)
    return df


def process_mp9_data():
    df = combine_mp9_csv(input_path)
    start,end = get_time_range(df)
    input, fail, failrate = get_fail_rate(df)
    list_fail_testers = list_testers(df[df['overallResult'] == 'FAIL'])
    tester_df = DataFrame(index=list_fail_testers, columns=['input', 'fail', 'failrate', 'fail_string', 'fail_detail'])
    for tester in list_fail_testers:
        input_, fail_, rate_ = get_fail_rate_by_tester(tester, df)
        fail_string_, spec_detail_ = get_mp9_fail_string(tester, df[df['overallResult'] == 'FAIL'])
        tester_df.loc[tester] = [input_, fail_, rate_, fail_string_, spec_detail_]
    # print(tester_df)
    tester_df['failrate'] = tester_df['failrate'].str.rstrip('%').astype(float)
    sorter_df = tester_df.sort_values(by='failrate', ascending=False)
    sorter_df['failrate'] = sorter_df['failrate'].astype(str) + '%'
    sorter_df.to_csv(os.path.join(out_folder_name, "fail_tester_MP9.csv"), index=True)
    info_label.config(text=f"time range:[{start}~{end}],MP9 overall retest :{failrate} ({fail}R/{input}T)")


def process_data():
    info_label.config(text="")
    if not input_path:
        info_label.config(text="input folder not selected！")
        return
    if not output_path:
        info_label.config(text="output folder not selected！")
        return
    create_folder()
    select_station = var0.get()
    if select_station == 'TSP':
        process_tsp_data()
    elif select_station == 'DVA':
        process_dva_data()
    elif select_station == 'MP9':
        process_mp9_data()


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
    # TRIAL_END_DATE = datetime(2024, 4, 1, 00, 00, 00)
    # if  now > TRIAL_END_DATE:
    #     return True
    license_path = os.path.join(Path(__file__).parent.resolve(), "license.txt")
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


def insert_text(local_):
    local_file.config(state='normal', bg='#303030', fg='white')
    local_file.insert(1.0, local_ + '\n')
    local_file.config(state='disabled', bg='#303030', fg='white')


def start_thread():
    t = threading.Thread(target=process_data)
    t.start()


root = Tk()
if is_overdated():
    root.withdraw()
    messagebox.showinfo("hint", "license expired！")
root.geometry("900x300+100+100")
root.title("Data analyzer")
input_label = Label(root, width=24, text="please select the input folder  ")
input_label.grid(row=1, column=1, columnspan=3, sticky='w')
input_button = Button(root, text="input csv folder", command=select_csv_file)
input_button.grid(row=1, column=0, sticky='ew')
input_path = ""

output_label = Label(root, width=24, text="please select the output folder")
output_label.grid(row=2, column=1, columnspan=3, sticky='w')
output_button = Button(root, text="output folder", command=select_output_path)
output_button.grid(row=2, column=0, sticky='ew')
output_path = ""

process_button = Button(root, text="process data", command=start_thread)
process_button.grid(row=3, column=0, sticky='ew')

radio_frame = Frame(root)
radio_frame.grid(row=3, column=1)
var0 = StringVar()
radio1 = Radiobutton(radio_frame, text="TSP", value="TSP", variable=var0)
radio1.grid(row=0, column=0, sticky='w')
radio2 = Radiobutton(radio_frame, text="DVA", value="DVA", variable=var0)
radio2.grid(row=0, column=1, sticky='w')
radio3 = Radiobutton(radio_frame, text="MP9", value="MP9", variable=var0)
radio3.grid(row=0, column=2, sticky='w')
var0.set('TSP')

info_label = Label(root, text=" ")
info_label.grid(row=9, column=0, columnspan=5)

local_file = Text(root, width=125, height=14)
local_file.config(state='disabled', bg='#303030', fg='white')
local_file.grid(row=10, column=0, columnspan=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
