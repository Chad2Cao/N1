import threading #line:1:import threading
import warnings #line:2:import warnings
import csv #line:3:import csv
import os #line:4:import os
from pathlib import Path #line:5:from pathlib import Path
from datetime import datetime #line:6:from datetime import datetime
from tkinter import filedialog ,messagebox #line:7:from tkinter import filedialog, messagebox
from pandas import DataFrame ,read_csv ,concat ,isnull ,to_datetime #line:8:from pandas import DataFrame, read_csv, concat, isnull, to_datetime
from tkinter import Tk ,Label ,Button ,Radiobutton ,Frame ,StringVar ,Text #line:9:from tkinter import Tk, Label, Button, Radiobutton, Frame, StringVar, Text
import base64 #line:10:import base64
from Crypto .Cipher import DES #line:11:from Crypto.Cipher import DES
global folder ,program_folder #line:13:global folder, program_folder
folder =Path (__file__ ).parent .resolve ()#line:14:folder = Path(__file__).parent.resolve()
folder =folder .parent .parent .parent #line:17:folder = folder.parent.parent.parent  # change to this when package
warnings .filterwarnings ('ignore')#line:19:warnings.filterwarnings('ignore')
def on_closing ():#line:20:def on_closing():
    root .destroy ()#line:22:root.destroy()
def select_csv_file ():#line:25:def select_csv_file():
    global input_path #line:26:global input_path
    input_path =filedialog .askdirectory (title ="please select the input folder",initialdir =os .path .join (folder ,'csv'))#line:27:input_path = filedialog.askdirectory(title="please select the input folder", initialdir=os.path.join(folder, 'csv'))
    input_label .config (text =input_path )#line:28:input_label.config(text=input_path)
def select_output_path ():#line:31:def select_output_path():
    global output_path #line:32:global output_path
    output_path =filedialog .askdirectory (title ="please select output folder",initialdir =folder )#line:33:output_path = filedialog.askdirectory(title="please select output folder", initialdir=folder)
    output_label .config (text =output_path )#line:34:output_label.config(text=output_path)
def create_folder ():#line:37:def create_folder():
    OO0000000O0OOOO0O =datetime .now ()#line:38:now = datetime.now()
    OOOO00000O0OOO00O =OO0000000O0OOOO0O .strftime ("%Y-%m-%d_%H-%M-%S")#line:41:time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    global out_folder_name #line:44:global out_folder_name
    out_folder_name =os .path .join (output_path ,OOOO00000O0OOO00O )#line:45:out_folder_name = os.path.join(output_path, time_str)
    os .makedirs (out_folder_name )#line:46:os.makedirs(out_folder_name)
def tsp_Probe_key_list ():#line:49:def tsp_Probe_key_list():
    OO00OO0000OOO000O =[]#line:50:probe_key_list = []
    O0O00OO0O00OOO0OO =os .path .join (Path (__file__ ).parent .resolve (),'key_for_probe.csv')#line:51:file_path = os.path.join(Path(__file__).parent.resolve(), 'key_for_probe.csv')
    with open (O0O00OO0O00OOO0OO ,'r',encoding ='utf-8')as O000OOOO00OOO0O0O :#line:53:with open(file_path, 'r', encoding='utf-8') as csvfile:
        OOO0O0O000O000O0O =csv .reader (O000OOOO00OOO0O0O )#line:55:csv_reader = csv.reader(csvfile)
        next (OOO0O0O000O000O0O )#line:56:next(csv_reader)
        for O0O000OOOO0OOOO0O in OOO0O0O000O000O0O :#line:58:for row in csv_reader:
            O00O00O0O0O0O0O0O ={'key':O0O000OOOO0OOOO0O [0 ],'spec':O0O000OOOO0OOOO0O [1 ],'probe':O0O000OOOO0OOOO0O [2 ]}#line:59:key_dict = {'key': row[0], 'spec': row[1], 'probe': row[2]}
            OO00OO0000OOO000O .append (O00O00O0O0O0O0O0O )#line:60:probe_key_list.append(key_dict)
    return OO00OO0000OOO000O #line:61:return probe_key_list
def Spec_key_list ():#line:64:def Spec_key_list():
    OO000OO0000OO000O =[]#line:65:spec_key_list = []
    OOOOOO0OOO0OO0OO0 =os .path .join (Path (__file__ ).parent .resolve (),'key_for_spec.csv')#line:66:file_path = os.path.join(Path(__file__).parent.resolve(), 'key_for_spec.csv')
    with open (OOOOOO0OOO0OO0OO0 ,'r',encoding ='utf-8')as O00O0OOO0O00OO000 :#line:67:with open(file_path, 'r', encoding='utf-8') as csvfile:
        OO0OO0000O0O0O000 =csv .reader (O00O0OOO0O00OO000 )#line:69:csv_reader = csv.reader(csvfile)
        next (OO0OO0000O0O0O000 )#line:70:next(csv_reader)
        for O0O00OO00O000O00O in OO0OO0000O0O0O000 :#line:72:for row in csv_reader:
            O00OO000OO0OOO00O ={'key':O0O00OO00O000O00O [0 ],'spec':O0O00OO00O000O00O [1 ]}#line:73:key_dict = {'key': row[0], 'spec': row[1]}
            OO000OO0000OO000O .append (O00OO000OO0OOO00O )#line:74:spec_key_list.append(key_dict)
    return OO000OO0000OO000O #line:75:return spec_key_list
def isTSPlog (O0O00000OOO0OO00O ):#line:78:def isTSPlog(filename_):
    if O0O00000OOO0OO00O .startswith ('TSP_')and O0O00000OOO0OO00O .endswith ('.csv'):#line:79:if filename_.startswith('TSP_') and filename_.endswith('.csv'):
        return True #line:80:return True
    else :#line:81:else:
        return False #line:82:return False
def combine_tsp_csv (OOO00O000OO000OO0 ):#line:85:def combine_tsp_csv(input_path):
    O00OO000OO00000O0 =DataFrame ()#line:86:df = DataFrame()
    for OOO0O0O00O0000OOO in os .listdir (OOO00O000OO000OO0 ):#line:87:for filename in os.listdir(input_path):
        if isTSPlog (OOO0O0O00O0000OOO ):#line:88:if isTSPlog(filename):
            O00000OOO00OO0OOO =os .path .join (OOO00O000OO000OO0 ,OOO0O0O00O0000OOO )#line:89:file_path = os.path.join(input_path, filename)
            insert_text ('combining：'+OOO0O0O00O0000OOO )#line:91:insert_text('combining：' + filename)
            O0OOOO0OO0OOO0O0O =read_csv (O00000OOO00OO0OOO ,header =1 ,na_values =['NA'],dtype ={'FIRST_FAILED_SPEC':str ,'TesterID':str ,'errCode':str ,'FIXTURE_ID':str })#line:93:dtype={'FIRST_FAILED_SPEC': str, 'TesterID': str, 'errCode': str, 'FIXTURE_ID': str})
            O0OOOO0OO0OOO0O0O .drop (range (0 ,2 ),inplace =True )#line:94:ori_data.drop(range(0, 2), inplace=True)
            O0OOOOOOOOOOO00O0 =['SerialNumber','overallResult','errCode','errString','FIRST_FAILED_SPEC','startTime','stopTime','TesterID','testTime','SW_VER','CONFIG','TEST_SCRIPT','FIXTURE_ID','macOS','macMini','macRAM','PROJECT','COMP_VER','SpecVersion','MALIBU_FW_VERSION','BRIDGE_FW_VER','HERON_FW','DUT_FW_VER','CARRIER_PN','CARRIER_MAX_RUN','CARRIER_TOTAL_TEST','CARRIER_UNIT_FAIL','CARRIER_LOCK_STATUS']#line:100:'CARRIER_LOCK_STATUS']
            O0OOOOOO00OO00OOO =O0OOOO0OO0OOO0O0O [O0OOOOOOOOOOO00O0 ]#line:101:data = ori_data[keep_columns]
            O0OOOOOO00OO00OOO =O0OOOOOO00OO00OOO .dropna (subset =['SerialNumber'])#line:102:data = data.dropna(subset=['SerialNumber'])  # Return a new Series with missing values removed.
            O0OOOOOO00OO00OOO .loc [:,'first_failed_value']=""#line:103:data.loc[:, 'first_failed_value'] = ""
            O0OOOOOO00OO00OOO .loc [:,'first_failed_spec']=""#line:104:data.loc[:, 'first_failed_spec'] = ""
            O0OOOOOO00OO00OOO .loc [:,'first_failed_probe']=""#line:105:data.loc[:, 'first_failed_probe'] = ""
            for OO0OOO00O00OOOOOO ,OO0000OOOOOO0OO00 in O0OOOO0OO0OOO0O0O .iterrows ():#line:107:for index, row in ori_data.iterrows():
                if OO0000OOOOOO0OO00 ['overallResult']=='FAIL':#line:108:if row['overallResult'] == 'FAIL':
                    OO000000O00OO0OOO =OO0000OOOOOO0OO00 ['FIRST_FAILED_SPEC']#line:109:key = row['FIRST_FAILED_SPEC']
                    try :#line:110:try:
                        O0000OO00O000OOO0 =OO0000OOOOOO0OO00 [OO000000O00OO0OOO ]#line:112:value = row[key]
                    except KeyError :#line:113:except KeyError:
                        O0000OO00O000OOO0 ="NA"#line:115:value = "NA"
                    except Exception as OOO00O00OOO0OO000 :#line:116:except Exception as e:
                        print ("error：",str (OOO00O00OOO0OO000 ))#line:118:print("error：", str(e))
                    O0OOOOOO00OO00OOO .loc [OO0OOO00O00OOOOOO ,'first_failed_value']=O0000OO00O000OOO0 #line:119:data.loc[index, 'first_failed_value'] = value
                    OOOO0OO0O0OOOO000 =tsp_Probe_key_list ()#line:124:probe_key_list = tsp_Probe_key_list()
                    for OO00OO0000OO00O00 in OOOO0OO0O0OOOO000 :#line:125:for d in probe_key_list:
                        if OO000000O00OO0OOO ==OO00OO0000OO00O00 ['key']:#line:126:if key == d['key']:
                            O0OOOOOO00OO00OOO .loc [OO0OOO00O00OOOOOO ,'first_failed_probe']=OO00OO0000OO00O00 ['probe']#line:127:data.loc[index, 'first_failed_probe'] = d['probe']
                            O0OOOOOO00OO00OOO .loc [OO0OOO00O00OOOOOO ,'first_failed_spec']=OO00OO0000OO00O00 ['spec']#line:128:data.loc[index, 'first_failed_spec'] = d['spec']
            O0OOOOOO00OO00OOO ['SerialNumber']=O0OOOOOO00OO00OOO ['SerialNumber'].str .split ("+").str [0 ]#line:130:data['SerialNumber'] = data['SerialNumber'].str.split("+").str[0]
            O0OOOOOO00OO00OOO .rename (columns ={'startTime':'StartTime'},inplace =True )#line:131:data.rename(columns={'startTime': 'StartTime'}, inplace=True)
            O00OO000OO00000O0 =concat ([O00OO000OO00000O0 ,O0OOOOOO00OO00OOO ],ignore_index =True )#line:132:df = concat([df, data], ignore_index=True)
    O00OO000OO00000O0 .to_csv (os .path .join (out_folder_name ,"combine.csv"),index =False )#line:134:df.to_csv(os.path.join(out_folder_name, "combine.csv"), index=False)
    return O00OO000OO00000O0 #line:135:return df
def get_from_filename (O00OOO000OOO0OO00 :str ):#line:138:def get_from_filename(filename: str):
    O0OO0O00000OOO0OO =O00OOO000OOO0OO00 .split ('_')[3 ]#line:139:tester_id = filename.split('_')[3]
    return f'DVA-{O0OO0O00000OOO0OO}'#line:140:return f'DVA-{tester_id}'
def isDVAlog (O000OO0000OOO00O0 ):#line:143:def isDVAlog(filename_):
    if O000OO0000OOO00O0 .endswith ('.csv')and O000OO0000OOO00O0 .startswith ('Summary_')and 'IQC-DISPLAY-3'in O000OO0000OOO00O0 :#line:144:if filename_.endswith('.csv') and filename_.startswith('Summary_') and 'IQC-DISPLAY-3' in filename_:
        return True #line:145:return True
    else :#line:146:else:
        return False #line:147:return False
def combine_dva_csv (OO0O000O0O0OO0O0O ):#line:150:def combine_dva_csv(input_path):
    O0OOOOO0O0OO00OOO =DataFrame ()#line:151:df = DataFrame()
    for O0OOO00O0OOO00000 in os .listdir (OO0O000O0O0OO0O0O ):#line:152:for filename in os.listdir(input_path):
        if isDVAlog (O0OOO00O0OOO00000 ):#line:153:if isDVAlog(filename):
            O0O00OOOO0OO0OO0O =os .path .join (OO0O000O0O0OO0O0O ,O0OOO00O0OOO00000 )#line:154:file_path = os.path.join(input_path, filename)
            insert_text ('combining：'+O0OOO00O0OOO00000 )#line:155:insert_text('combining：' + filename)
            OO00O00OO00O000OO =read_csv (O0O00OOOO0OO0OO0O ,header =0 ,na_values =['NA'],dtype ={'FIXTURE_ID':str ,'FailedTestName':str ,'FailedValue':float ,'FailedUL':str ,'FailedLL':str ,'Fail Type':str })#line:158:'FailedLL': str, 'Fail Type': str})
            OOO0O0000OOO0OO0O =['SerialNumber','StartTime','FailedTestName','FailedValue','FailedUL','FailedLL','Fail Type','Head Id','cameraSN','carrierSN','softwareversion']#line:161:'Fail Type', 'Head Id', 'cameraSN', 'carrierSN', 'softwareversion']
            O0O0OO0O00OO00OOO =OO00O00OO00O000OO [OOO0O0000OOO0OO0O ]#line:162:data = ori_data[keep_columns]
            O0O0OO0O00OO00OOO =O0O0OO0O00OO00OOO .dropna (subset =['SerialNumber'])#line:163:data = data.dropna(subset=['SerialNumber'])  # Return a new Series with missing values removed.
            O0O0OO0O00OO00OOO .rename (columns ={'FailedTestName':'errString'},inplace =True )#line:164:data.rename(columns={'FailedTestName': 'errString'}, inplace=True)
            O0O0OO0O00OO00OOO .rename (columns ={'carrierSN':'CARRIER_PN'},inplace =True )#line:165:data.rename(columns={'carrierSN': 'CARRIER_PN'}, inplace=True)
            O0O0OO0O00OO00OOO .loc [:,'TesterID']=get_from_filename (O0OOO00O0OOO00000 )#line:167:data.loc[:, 'TesterID'] = get_from_filename(filename)
            O0O0OO0O00OO00OOO ['overallResult']=O0O0OO0O00OO00OOO .apply (lambda O00OO00O0O0OO000O :'PASS'if isnull (O00OO00O0O0OO000O ['errString'])else 'FAIL',axis =1 )#line:172:data['overallResult'] = data.apply(lambda row: 'PASS' if isnull(row['errString']) else 'FAIL', axis=1)
            O0OOOOO0O0OO00OOO =concat ([O0OOOOO0O0OO00OOO ,O0O0OO0O00OO00OOO ],ignore_index =True )#line:173:df = concat([df, data], ignore_index=True)
    return O0OOOOO0O0OO00OOO #line:175:return df
def get_input_count_of_tester (O0OOOOOO0OOO0OOO0 ,OOOO0O0OOOO0O00OO ):#line:178:def get_input_count_of_tester(tester, df):
    return OOOO0O0OOOO0O00OO [OOOO0O0OOOO0O00OO ['TesterID']==O0OOOOOO0OOO0OOO0 ]['SerialNumber'].nunique ()#line:179:return df[df['TesterID'] == tester]['SerialNumber'].nunique()
def get_fail_rate (O00OOOO000O00OO00 ):#line:182:def get_fail_rate(df):
    O00OOO0O0O0000OO0 =O00OOOO000O00OO00 ['SerialNumber'].nunique ()#line:184:input = df['SerialNumber'].nunique()
    OO00OO000000000O0 =O00OOOO000O00OO00 [O00OOOO000O00OO00 ['overallResult']=='FAIL']['SerialNumber'].nunique ()#line:185:fail = df[df['overallResult'] == 'FAIL']['SerialNumber'].nunique()
    if O00OOO0O0O0000OO0 ==0 :#line:186:if input == 0:
        return 0 ,0 ,0 #line:187:return 0, 0, 0
    O00OO000O00O000O0 =format ((OO00OO000000000O0 /O00OOO0O0O0000OO0 ),'.2%')#line:188:rate = format((fail / input), '.2%')
    return O00OOO0O0O0000OO0 ,OO00OO000000000O0 ,O00OO000O00O000O0 #line:189:return input, fail, rate
def top_fail_testers (O0OO00O0000O00OOO ,OOOO0O0OO0000OOOO ):#line:192:def top_fail_testers(df, top):
    OOOO00O00O0OOO0O0 =O0OO00O0000O00OOO ['TesterID'].value_counts ().head (OOOO0O0OO0000OOOO ).index .tolist ()#line:193:top_tester = df['TesterID'].value_counts().head(top).index.tolist()
    return OOOO00O00O0OOO0O0 #line:194:return top_tester
def top_fail_failures (O0O00O0O0OOO0OOOO ,OOO00OOOO00OO00O0 ):#line:197:def top_fail_failures(df, top):
    OOO00OO0O0O00OOO0 =O0O00O0O0OOO0OOOO ['errString'].value_counts ().head (OOO00OOOO00OO00O0 )#line:198:top_failure = df['errString'].value_counts().head(top)
    return OOO00OO0O0O00OOO0 #line:199:return top_failure
def top_first_fail_spec (OO00O00O0000O0O00 ,O0OOOO0O0000O0OOO ):#line:202:def top_first_fail_spec(df, top):
    OO000O0000000O00O =OO00O00O0000O0O00 ['FIRST_FAILED_SPEC'].value_counts ().head (O0OOOO0O0000O0OOO )#line:203:top_failure = df['FIRST_FAILED_SPEC'].value_counts().head(top)
    return OO000O0000000O00O #line:204:return top_failure
def get_fail_rate_by_tester (OO00O00OOO000OO00 ,O0O0OO00O0O000O00 ):#line:207:def get_fail_rate_by_tester(tester, df):
    O0O0OO00O0O000O00 =O0O0OO00O0O000O00 [O0O0OO00O0O000O00 ['TesterID']==OO00O00OOO000OO00 ]#line:209:df = df[df['TesterID'] == tester]
    return get_fail_rate (O0O0OO00O0O000O00 )#line:210:return get_fail_rate(df)
def list_testers (OOOOOOO00O00000O0 ):#line:213:def list_testers(df):
    return OOOOOOO00O00000O0 ['TesterID'].value_counts ().index .tolist ()#line:215:return df['TesterID'].value_counts().index.tolist()
def get_tsp_fail_string (OOOOOO0O0O00OO0O0 ,OO00O0O000OO0OO00 ):#line:218:def get_tsp_fail_string(tester, df):
    OO00O0O000OO0OO00 =OO00O0O000OO0OO00 [OO00O0O000OO0OO00 ['TesterID']==OOOOOO0O0O00OO0O0 ]#line:219:df = df[df['TesterID'] == tester]
    O000OO0O0O00OOOO0 =''#line:220:fail_string = ''
    O000OO00OOOO0OO0O =''#line:221:spec_detail = ''
    for OOO0O0OOO000OOOOO ,OOOO000O000OOO0O0 in top_fail_failures (OO00O0O000OO0OO00 ,5 ).items ():#line:222:for index, value in top_fail_failures(df, 5).items():
        OO0000OOO00O0OO00 =OO00O0O000OO0OO00 [OO00O0O000OO0OO00 ['errString']==OOO0O0OOO000OOOOO ]['errCode'].tolist ()[0 ]#line:223:code = df[df['errString'] == index]['errCode'].tolist()[0]
        O000OO0O0O00OOOO0 +=f"{OO0000OOO00O0OO00}_{OOO0O0OOO000OOOOO}:{OOOO000O000OOO0O0}R\n"#line:226:fail_string += f"{code}_{index}:{value}R\n"
    for OOO0O0OOO000OOOOO ,OOOO000O000OOO0O0 in top_first_fail_spec (OO00O0O000OO0OO00 ,5 ).items ():#line:227:for index, value in top_first_fail_spec(df, 5).items():
        if OOO0O0OOO000OOOOO in [O00O000OOO00OOOOO ['key']for O00O000OOO00OOOOO in tsp_Probe_key_list ()]:#line:228:if index in [d['key'] for d in tsp_Probe_key_list()]:
            OOOO0000O0OOOOO0O =OO00O0O000OO0OO00 [OO00O0O000OO0OO00 ['FIRST_FAILED_SPEC']==OOO0O0OOO000OOOOO ]['first_failed_probe'].tolist ()[0 ]#line:229:probe = df[df['FIRST_FAILED_SPEC'] == index]['first_failed_probe'].tolist()[0]
            O000OO0OO00OO0O0O =OO00O0O000OO0OO00 [OO00O0O000OO0OO00 ['FIRST_FAILED_SPEC']==OOO0O0OOO000OOOOO ]['first_failed_value'].tolist ()#line:230:failed_value = df[df['FIRST_FAILED_SPEC'] == index]['first_failed_value'].tolist()
            OO0O0OOOO0O00OO0O =tuple ([round (OOOOOOOO0O000OOO0 ,2 )for OOOOOOOO0O000OOO0 in O000OO0OO00OO0O0O ])#line:231:failed_value_round = tuple([round(x, 2) for x in failed_value])
            OO00OOO0O0OOO0OO0 =OO00O0O000OO0OO00 [OO00O0O000OO0OO00 ['FIRST_FAILED_SPEC']==OOO0O0OOO000OOOOO ]['first_failed_spec'].tolist ()[0 ]#line:232:spec = df[df['FIRST_FAILED_SPEC'] == index]['first_failed_spec'].tolist()[0]
            O000OO00OOOO0OO0O +=f"{OOO0O0OOO000OOOOO}:{OOOO000O000OOO0O0}R -->value:{OO0O0OOOO0O00OO0O}{OO00OOO0O0OOO0OO0}@{OOOO0000O0OOOOO0O}\n"#line:234:spec_detail += f"{index}:{value}R -->value:{failed_value_round}{spec}@{probe}\n"
    return O000OO0O0O00OOOO0 ,O000OO00OOOO0OO0O #line:235:return fail_string, spec_detail
def get_dva_fail_string (O0000OOOO0OOO0O00 ,O00O000O000OO0O00 ):#line:238:def get_dva_fail_string(tester, df):
    O00O000O000OO0O00 =O00O000O000OO0O00 [O00O000O000OO0O00 ['TesterID']==O0000OOOO0OOO0O00 ]#line:239:df = df[df['TesterID'] == tester]
    O0000O0OOOO0OO00O =''#line:240:fail_string = ''
    O000OOO0O0O0OO0OO =''#line:241:fail_detail = ''
    for O0O0O0OOOO0O0OOOO ,OOOO0O0OOOO000OOO in top_fail_failures (O00O000O000OO0O00 ,5 ).items ():#line:242:for index, value in top_fail_failures(df, 5).items():
        O0OOO0000O00OO000 =O00O000O000OO0O00 [O00O000O000OO0O00 ['errString']==O0O0O0OOOO0O0OOOO ]['FailedValue'].tolist ()#line:243:failed_value = df[df['errString'] == index]['FailedValue'].tolist()
        OO000O00O00O000OO =tuple ([round (OO00OOO000O0O0O00 ,2 )for OO00OOO000O0O0O00 in O0OOO0000O00OO000 ])#line:244:failed_value_round = tuple([round(x, 2) for x in failed_value])
        O0OOO0000000O00O0 =O00O000O000OO0O00 [O00O000O000OO0O00 ['errString']==O0O0O0OOOO0O0OOOO ]['FailedUL'].tolist ()[0 ]#line:245:UL = df[df['errString'] == index]['FailedUL'].tolist()[0]
        O0OOOO0OOO0O0OO00 =O00O000O000OO0O00 [O00O000O000OO0O00 ['errString']==O0O0O0OOOO0O0OOOO ]['FailedLL'].tolist ()[0 ]#line:246:LL = df[df['errString'] == index]['FailedLL'].tolist()[0]
        O0000O0OOOO0OO00O +=f"{O0O0O0OOOO0O0OOOO}:{OOOO0O0OOOO000OOO}R\n"#line:248:fail_string += f"{index}:{value}R\n"
        O000OOO0O0O0OO0OO +=f"{O0O0O0OOOO0O0OOOO}:{OO000O00O00O000OO}[{O0OOOO0OOO0O0OO00}~{O0OOO0000000O00O0}]\n"#line:249:fail_detail += f"{index}:{failed_value_round}[{LL}~{UL}]\n"
    return O0000O0OOOO0OO00O ,O000OOO0O0O0OO0OO #line:251:return fail_string, fail_detail
def get_mp9_fail_string (OOO00OOO0O0O0O00O ,O0OOO0000OOO0OOO0 ):#line:254:def get_mp9_fail_string(tester, df):
    O0OOO0000OOO0OOO0 =O0OOO0000OOO0OOO0 [O0OOO0000OOO0OOO0 ['TesterID']==OOO00OOO0O0O0O00O ]#line:255:df = df[df['TesterID'] == tester]
    OOOOOOO0OO0OOO000 =''#line:256:fail_string = ''
    OOOO0O0O0OO000OOO =''#line:257:spec_detail = ''
    for O0OO000000O000OO0 ,OO0OOOO00OO0O0O00 in top_fail_failures (O0OOO0000OOO0OOO0 ,5 ).items ():#line:258:for index, value in top_fail_failures(df, 5).items():
        OOOOOOO0OO0OOO000 +=f"{O0OO000000O000OO0}:{OO0OOOO00OO0O0O00}R\n"#line:259:fail_string += f"{index}:{value}R\n"
        if O0OO000000O000OO0 in [O00OO000OO0O0OOOO ['key']for O00OO000OO0O0OOOO in mp9_key_list ()]:#line:260:if index in [d['key'] for d in mp9_key_list()]:
            O00OO0O0OOO0000O0 =O0OOO0000OOO0OOO0 [O0OOO0000OOO0OOO0 ['errString']==O0OO000000O000OO0 ]['first_failed_value'].tolist ()#line:261:failed_value = df[df['errString'] == index]['first_failed_value'].tolist()
            OO000OOOOO0OO0O00 =[float (OO00000O0OO0O0OOO )for OO00000O0OO0O0OOO in O00OO0O0OOO0000O0 ]#line:262:failed_list = [float(x) for x in failed_value]
            O00000OOOOO00000O =tuple ([round (OO0OOO0000O00O0O0 ,2 )for OO0OOO0000O00O0O0 in OO000OOOOO0OO0O00 ])#line:263:failed_value_round = tuple([round(x, 2) for x in failed_list])
            OOOO0O0O00O0O0OOO =O0OOO0000OOO0OOO0 [O0OOO0000OOO0OOO0 ['errString']==O0OO000000O000OO0 ]['first_failed_spec'].tolist ()[0 ]#line:264:spec = df[df['errString'] == index]['first_failed_spec'].tolist()[0]
            OOOO0O0O0OO000OOO +=f"{O0OO000000O000OO0}-->value:{O00000OOOOO00000O}{OOOO0O0O00O0O0OOO}\n"#line:265:spec_detail += f"{index}-->value:{failed_value_round}{spec}\n"
    return OOOOOOO0OO0OOO000 ,OOOO0O0O0OO000OOO #line:267:return fail_string, spec_detail
def get_time_range (O00OO0O00O0OOO0O0 ):#line:270:def get_time_range(df):
    O00OO0O00O0OOO0O0 ['StartTime']=to_datetime (O00OO0O00O0OOO0O0 ['StartTime'])#line:271:df['StartTime'] = to_datetime(df['StartTime'])
    O00OO0O00O0OOO0O0 =O00OO0O00O0OOO0O0 .sort_values ('StartTime')#line:272:df = df.sort_values('StartTime')
    O0O000OO00OOOOOO0 =O00OO0O00O0OOO0O0 ['StartTime'].head (1 ).values [0 ].astype (str ).split ('.')[0 ].replace ('T',' ')#line:273:start = df['StartTime'].head(1).values[0].astype(str).split('.')[0].replace('T',' ')
    O0OOOOOO00000O000 =O00OO0O00O0OOO0O0 ['StartTime'].tail (1 ).values [0 ].astype (str ).split ('.')[0 ].replace ('T',' ')#line:274:end = df['StartTime'].tail(1).values[0].astype(str).split('.')[0].replace('T',' ')
    return O0O000OO00OOOOOO0 ,O0OOOOOO00000O000 #line:275:return start, end
def process_tsp_data ():#line:278:def process_tsp_data():
    O00O0OO00O0O0OO00 =combine_tsp_csv (input_path )#line:279:df = combine_tsp_csv(input_path)
    O0000OO0000OOO000 ,O00O000OO0000OO0O =get_time_range (O00O0OO00O0O0OO00 )#line:280:start, end = get_time_range(df)
    OO00O0OOO00000O0O ,O00OO0OOO00OOOO0O ,O0OOO0OOOOOO000OO =get_fail_rate (O00O0OO00O0O0OO00 )#line:281:input, fail, failrate = get_fail_rate(df)
    O000OO0O0000OOOO0 =list_testers (O00O0OO00O0O0OO00 [O00O0OO00O0O0OO00 ['overallResult']=='FAIL'])#line:284:list_fail_testers = list_testers(df[df['overallResult'] == 'FAIL'])
    O00O00OOOO0OOOO00 =DataFrame (index =O000OO0O0000OOOO0 ,columns =['input','fail','failrate','fail_string','fail_detail'])#line:285:tester_df = DataFrame(index=list_fail_testers, columns=['input', 'fail', 'failrate', 'fail_string', 'fail_detail'])
    for O000O0OO0OOOO0OOO in O000OO0O0000OOOO0 :#line:287:for tester in list_fail_testers:
        OO0O000OO0O00O0O0 ,O00O0OO0OO0O00O0O ,O0000000OOO00OO0O =get_fail_rate_by_tester (O000O0OO0OOOO0OOO ,O00O0OO00O0O0OO00 )#line:288:input_, fail_, rate_ = get_fail_rate_by_tester(tester, df)
        OOO000O0O0O0O000O ,O0OO0O0OOOOO0O0O0 =get_tsp_fail_string (O000O0OO0OOOO0OOO ,O00O0OO00O0O0OO00 [O00O0OO00O0O0OO00 ['overallResult']=='FAIL'])#line:289:fail_string_, spec_detail_ = get_tsp_fail_string(tester, df[df['overallResult'] == 'FAIL'])
        O00O00OOOO0OOOO00 .loc [O000O0OO0OOOO0OOO ]=[OO0O000OO0O00O0O0 ,O00O0OO0OO0O00O0O ,O0000000OOO00OO0O ,OOO000O0O0O0O000O ,O0OO0O0OOOOO0O0O0 ]#line:290:tester_df.loc[tester] = [input_, fail_, rate_, fail_string_, spec_detail_]
    O00O00OOOO0OOOO00 ['failrate']=O00O00OOOO0OOOO00 ['failrate'].str .rstrip ('%').astype (float )#line:292:tester_df['failrate'] = tester_df['failrate'].str.rstrip('%').astype(float)
    O0OO000OOO0OOOOO0 =O00O00OOOO0OOOO00 .sort_values (by ='failrate',ascending =False )#line:293:sorter_df = tester_df.sort_values(by='failrate', ascending=False)
    O0OO000OOO0OOOOO0 ['failrate']=O0OO000OOO0OOOOO0 ['failrate'].astype (str )+'%'#line:294:sorter_df['failrate'] = sorter_df['failrate'].astype(str) + '%'
    O0OO000OOO0OOOOO0 .to_csv (os .path .join (out_folder_name ,"fail_tester_TSP.csv"),index =True )#line:295:sorter_df.to_csv(os.path.join(out_folder_name, "fail_tester_TSP.csv"), index=True)
    info_label .config (text =f"time range:[{O0000OO0000OOO000}~{O00O000OO0000OO0O}], TSP-E overall retest:{O0OOO0OOOOOO000OO} ({O00OO0OOO00OOOO0O}R/{OO00O0OOO00000O0O}T)")#line:296:info_label.config(text=f"time range:[{start}~{end}], TSP-E overall retest:{failrate} ({fail}R/{input}T)")
def process_dva_data ():#line:299:def process_dva_data():
    O00O0OO0OOO0O0O0O =combine_dva_csv (input_path )#line:300:df = combine_dva_csv(input_path)
    O0000O0OO0O0000OO ,O00OOOOO00OOO0OOO =get_time_range (O00O0OO0OOO0O0O0O )#line:301:start, end = get_time_range(df)
    O00O000O0OOO0O000 ,O0O00OOO0O000OO00 ,OO0OO00OOO00O0OO0 =get_fail_rate (O00O0OO0OOO0O0O0O )#line:302:input, fail, failrate = get_fail_rate(df)
    OO000OO00O000O000 =list_testers (O00O0OO0OOO0O0O0O [O00O0OO0OOO0O0O0O ['overallResult']=='FAIL'])#line:305:list_fail_testers = list_testers(df[df['overallResult'] == 'FAIL'])
    OO0000O0000OOOO0O =DataFrame (index =OO000OO00O000O000 ,columns =['input','fail','failrate','fail_string','probe_detail'])#line:306:tester_df = DataFrame(index=list_fail_testers, columns=['input', 'fail', 'failrate', 'fail_string', 'probe_detail'])
    for OO00OO0O0OOO0000O in OO000OO00O000O000 :#line:307:for tester in list_fail_testers:
        O00000O000OO00O00 ,O00OOO00O00O0OOOO ,OO0O0O0OO0OOO00OO =get_fail_rate_by_tester (OO00OO0O0OOO0000O ,O00O0OO0OOO0O0O0O )#line:308:input_, fail_, rate_ = get_fail_rate_by_tester(tester, df)
        O00O0OOO0000000O0 ,OO0O0OO0OO00O0O00 =get_dva_fail_string (OO00OO0O0OOO0000O ,O00O0OO0OOO0O0O0O [O00O0OO0OOO0O0O0O ['overallResult']=='FAIL'])#line:309:fail_string_, spec_detail_ = get_dva_fail_string(tester, df[df['overallResult'] == 'FAIL'])
        OO0000O0000OOOO0O .loc [OO00OO0O0OOO0000O ]=[O00000O000OO00O00 ,O00OOO00O00O0OOOO ,OO0O0O0OO0OOO00OO ,O00O0OOO0000000O0 ,OO0O0OO0OO00O0O00 ]#line:310:tester_df.loc[tester] = [input_, fail_, rate_, fail_string_, spec_detail_]
    OO0000O0000OOOO0O ['failrate']=OO0000O0000OOOO0O ['failrate'].str .rstrip ('%').astype (float )#line:312:tester_df['failrate'] = tester_df['failrate'].str.rstrip('%').astype(float)
    O0OOOOO0OOOO0O0OO =OO0000O0000OOOO0O .sort_values (by ='failrate',ascending =False )#line:313:sorter_df = tester_df.sort_values(by='failrate', ascending=False)
    O0OOOOO0OOOO0O0OO ['failrate']=O0OOOOO0OOOO0O0OO ['failrate'].astype (str )+'%'#line:314:sorter_df['failrate'] = sorter_df['failrate'].astype(str) + '%'
    O0OOOOO0OOOO0O0OO .to_csv (os .path .join (out_folder_name ,"fail_tester_DVA.csv"),index =True )#line:315:sorter_df.to_csv(os.path.join(out_folder_name, "fail_tester_DVA.csv"), index=True)
    info_label .config (text =f"time range:[{O0000O0OO0O0000OO}~{O00OOOOO00OOO0OOO}],DVA overall retest :{OO0OO00OOO00O0OO0} ({O0O00OOO0O000OO00}R/{O00O000O0OOO0O000}T)")#line:316:info_label.config(text=f"time range:[{start}~{end}],DVA overall retest :{failrate} ({fail}R/{input}T)")
def isMP9log (OO0OOOO0000O00000 ):#line:319:def isMP9log(filename):
    if OO0OOOO0000O00000 .endswith ('MP9.2_summary.csv'):#line:320:if filename.endswith('MP9.2_summary.csv'):
        return True #line:321:return True
    else :#line:322:else:
        return False #line:323:return False
def get_overallResult (O0000OO000OOOO0OO ):#line:326:def get_overallResult(row):
    if (O0000OO000OOOO0OO ['MP9 DMX1_Result']=='binA'and O0000OO000OOOO0OO ['MP9 DMX2_Result']=='binA'and O0000OO000OOOO0OO ['MP9 UNLD_Result']=='OK'and O0000OO000OOOO0OO ['MP9 Binning']=='binA'):#line:328:and row['MP9 Binning'] == 'binA'):
        return 'PASS'#line:329:return 'PASS'
    else :#line:330:else:
        return 'FAIL'#line:331:return 'FAIL'
def mp9_key_list ():#line:334:def mp9_key_list():
    OOOO0O00OOOO0O000 =[]#line:335:key_spec_list = []
    OOO0O0O0O00OOO0OO =os .path .join (Path (__file__ ).parent .resolve (),'mp9_key_spec.csv')#line:336:file_path = os.path.join(Path(__file__).parent.resolve(), 'mp9_key_spec.csv')
    with open (OOO0O0O0O00OOO0OO ,'r',encoding ='utf-8')as O00000O0OOOOOOOO0 :#line:337:with open(file_path, 'r', encoding='utf-8') as csvfile:
        O0OO0OOO000OOO0O0 =csv .reader (O00000O0OOOOOOOO0 )#line:339:csv_reader = csv.reader(csvfile)
        next (O0OO0OOO000OOO0O0 )#line:340:next(csv_reader)
        for OOO0OO0000OOO0O00 in O0OO0OOO000OOO0O0 :#line:342:for row in csv_reader:
            O00O0OOOO0O0OO0OO ={'key':OOO0OO0000OOO0O00 [0 ],'spec':f'[{OOO0OO0000OOO0O00[1]}~{OOO0OO0000OOO0O00[2]}]'}#line:343:key_dict = {'key': row[0], 'spec': f'[{row[1]}~{row[2]}]'}
            OOOO0O00OOOO0O000 .append (O00O0OOOO0O0OO0OO )#line:344:key_spec_list.append(key_dict)
    return OOOO0O00OOOO0O000 #line:345:return key_spec_list
def combine_mp9_csv (O00OOO0OOOO000000 ):#line:348:def combine_mp9_csv(input_path):
    O000O00O0O0OO00O0 =DataFrame ()#line:349:df = DataFrame()
    for O000O00OO0O0OO0OO in os .listdir (O00OOO0OOOO000000 ):#line:350:for filename in os.listdir(input_path):
        if isMP9log (O000O00OO0O0OO0OO ):#line:351:if isMP9log(filename):
            O00O0OOOO00OOO0OO =os .path .join (O00OOO0OOOO000000 ,O000O00OO0O0OO0OO )#line:352:file_path = os.path.join(input_path, filename)
            insert_text ('combining：'+O000O00OO0O0OO0OO )#line:353:insert_text('combining：' + filename)
            OOOO00000OOOO00O0 =read_csv (O00O0OOOO00OOO0OO ,header =0 ,na_values =['NA'],dtype ={'FIRST_FAILED_SPEC':str ,'TesterID':str ,'errCode':str ,'FIXTURE_ID':str })#line:356:'FIXTURE_ID': str})
            OOOO00000OOOO00O0 .drop (range (0 ,2 ),inplace =True )#line:357:ori_data.drop(range(0, 2), inplace=True)
            O0O00000O0O0000OO =['serialnumber','StartTime','StopTime','Test Time','StationID','NEST_ID','MP9 PM_Result','MP9 UNLD_Result','MP9 Test Pass/Fail','List_of_Failing_Items','MP9 DMX1_Result','MP9 DMX2_Result','MP9 Binning','softwareversion','MP9_CARRIER_SN']#line:361:'softwareversion', 'MP9_CARRIER_SN']
            O0O0O0OO000O0OO0O =OOOO00000OOOO00O0 [O0O00000O0O0000OO ]#line:362:data = ori_data[keep_columns]
            O0O0O0OO000O0OO0O .loc [:,'first_failed_key']=""#line:363:data.loc[:, 'first_failed_key'] = ""
            O0O0O0OO000O0OO0O .loc [:,'first_failed_value']=""#line:364:data.loc[:, 'first_failed_value'] = ""
            O0O0O0OO000O0OO0O .loc [:,'first_failed_spec']=""#line:365:data.loc[:, 'first_failed_spec'] = ""
            O0O0O0OO000O0OO0O ['overallResult']=O0O0O0OO000O0OO0O .apply (get_overallResult ,axis =1 )#line:366:data['overallResult'] = data.apply(get_overallResult, axis=1)
            for OOOOO0O0OOO00O00O ,OOO00000OO0OO0000 in OOOO00000OOOO00O0 .iterrows ():#line:368:for index, row in ori_data.iterrows():
                if O0O0O0OO000O0OO0O .loc [OOOOO0O0OOO00O00O ,'overallResult']=='FAIL':#line:369:if data.loc[index, 'overallResult'] == 'FAIL':
                    O00OOO0OOO00O0O0O =OOO00000OO0OO0000 ['List_of_Failing_Items'].split (';')[0 ]#line:370:key = row['List_of_Failing_Items'].split(';')[0]
                    O00OOO0OOO00O0O0O =O00OOO0OOO00O0O0O .replace (' CoF','')#line:371:key = key.replace(' CoF', '')
                    try :#line:372:try:
                        OOOOO000OOOO0OOOO =OOO00000OO0OO0000 [O00OOO0OOO00O0O0O ]#line:373:value = row[key]
                    except KeyError :#line:374:except KeyError:
                        OOOOO000OOOO0OOOO ="NA"#line:376:value = "NA"
                    except Exception as OO00O00OOOO0OO0O0 :#line:377:except Exception as e:
                        print ("发生错误：",str (OO00O00OOOO0OO0O0 ))#line:379:print("发生错误：", str(e))
                    O0O0O0OO000O0OO0O .loc [OOOOO0O0OOO00O00O ,'first_failed_key']=O00OOO0OOO00O0O0O #line:380:data.loc[index, 'first_failed_key'] = key
                    O0O0O0OO000O0OO0O .loc [OOOOO0O0OOO00O00O ,'first_failed_value']=OOOOO000OOOO0OOOO #line:381:data.loc[index, 'first_failed_value'] = value
                    O000OO000O0OOO000 =mp9_key_list ()#line:382:spec_list = mp9_key_list()
                    for OOO000O0OOO000O00 in O000OO000O0OOO000 :#line:383:for d in spec_list:
                        if O00OOO0OOO00O0O0O ==OOO000O0OOO000O00 ['key']:#line:384:if key == d['key']:
                            O0O0O0OO000O0OO0O .loc [OOOOO0O0OOO00O00O ,'first_failed_spec']=OOO000O0OOO000O00 ['spec']#line:385:data.loc[index, 'first_failed_spec'] = d['spec']
            O0O0O0OO000O0OO0O .rename (columns ={'serialnumber':'SerialNumber'},inplace =True )#line:386:data.rename(columns={'serialnumber': 'SerialNumber'}, inplace=True)
            O0O0O0OO000O0OO0O .rename (columns ={'StationID':'TesterID'},inplace =True )#line:387:data.rename(columns={'StationID': 'TesterID'}, inplace=True)
            O0O0O0OO000O0OO0O .rename (columns ={'MP9_CARRIER_SN':'CARRIER_PN'},inplace =True )#line:388:data.rename(columns={'MP9_CARRIER_SN': 'CARRIER_PN'}, inplace=True)
            O0O0O0OO000O0OO0O .rename (columns ={'first_failed_key':'errString'},inplace =True )#line:389:data.rename(columns={'first_failed_key': 'errString'}, inplace=True)
            O0O0O0OO000O0OO0O =O0O0O0OO000O0OO0O .dropna (subset =['SerialNumber','MP9 PM_Result','MP9 DMX1_Result','MP9 DMX2_Result'])#line:390:data = data.dropna(subset=['SerialNumber', 'MP9 PM_Result', 'MP9 DMX1_Result', 'MP9 DMX2_Result'])
            O0O0O0OO000O0OO0O ['CARRIER_PN']=O0O0O0OO000O0OO0O ['CARRIER_PN'].apply (lambda OOOO0OOOOO00O0O00 :'294100'+hex (int (OOOO0OOOOO00O0O00 ))[2 :].upper ())#line:391:data['CARRIER_PN'] = data['CARRIER_PN'].apply(lambda x: '294100' + hex(int(x))[2:].upper())
            O000O00O0O0OO00O0 =concat ([O000O00O0O0OO00O0 ,O0O0O0OO000O0OO0O ],ignore_index =True )#line:393:df = concat([df, data], ignore_index=True)
    return O000O00O0O0OO00O0 #line:395:return df
def process_mp9_data ():#line:398:def process_mp9_data():
    OO0O0OO00OOOO00O0 =combine_mp9_csv (input_path )#line:399:df = combine_mp9_csv(input_path)
    OOO0O000O0O0O000O ,O00O00O0000OO0000 =get_time_range (OO0O0OO00OOOO00O0 )#line:400:start,end = get_time_range(df)
    OOOOO0O000O00O000 ,O000O000O0000OOO0 ,OOO0OO0O0OO000000 =get_fail_rate (OO0O0OO00OOOO00O0 )#line:401:input, fail, failrate = get_fail_rate(df)
    OOO0O0O00OO0O00O0 =list_testers (OO0O0OO00OOOO00O0 [OO0O0OO00OOOO00O0 ['overallResult']=='FAIL'])#line:402:list_fail_testers = list_testers(df[df['overallResult'] == 'FAIL'])
    O0OO000O000OO0OOO =DataFrame (index =OOO0O0O00OO0O00O0 ,columns =['input','fail','failrate','fail_string','fail_detail'])#line:403:tester_df = DataFrame(index=list_fail_testers, columns=['input', 'fail', 'failrate', 'fail_string', 'fail_detail'])
    for O0O0O0O0O00000O00 in OOO0O0O00OO0O00O0 :#line:404:for tester in list_fail_testers:
        OOOO0O000OOO0OOOO ,O0OOO00O0000O0O00 ,O0000O0O00O0O0O00 =get_fail_rate_by_tester (O0O0O0O0O00000O00 ,OO0O0OO00OOOO00O0 )#line:405:input_, fail_, rate_ = get_fail_rate_by_tester(tester, df)
        O00OO0O00O0000OO0 ,O0O0O0OOO00O0O00O =get_mp9_fail_string (O0O0O0O0O00000O00 ,OO0O0OO00OOOO00O0 [OO0O0OO00OOOO00O0 ['overallResult']=='FAIL'])#line:406:fail_string_, spec_detail_ = get_mp9_fail_string(tester, df[df['overallResult'] == 'FAIL'])
        O0OO000O000OO0OOO .loc [O0O0O0O0O00000O00 ]=[OOOO0O000OOO0OOOO ,O0OOO00O0000O0O00 ,O0000O0O00O0O0O00 ,O00OO0O00O0000OO0 ,O0O0O0OOO00O0O00O ]#line:407:tester_df.loc[tester] = [input_, fail_, rate_, fail_string_, spec_detail_]
    O0OO000O000OO0OOO ['failrate']=O0OO000O000OO0OOO ['failrate'].str .rstrip ('%').astype (float )#line:409:tester_df['failrate'] = tester_df['failrate'].str.rstrip('%').astype(float)
    OOO0O0O000O000O00 =O0OO000O000OO0OOO .sort_values (by ='failrate',ascending =False )#line:410:sorter_df = tester_df.sort_values(by='failrate', ascending=False)
    OOO0O0O000O000O00 ['failrate']=OOO0O0O000O000O00 ['failrate'].astype (str )+'%'#line:411:sorter_df['failrate'] = sorter_df['failrate'].astype(str) + '%'
    OOO0O0O000O000O00 .to_csv (os .path .join (out_folder_name ,"fail_tester_MP9.csv"),index =True )#line:412:sorter_df.to_csv(os.path.join(out_folder_name, "fail_tester_MP9.csv"), index=True)
    info_label .config (text =f"time range:[{OOO0O000O0O0O000O}~{O00O00O0000OO0000}],MP9 overall retest :{OOO0OO0O0OO000000} ({O000O000O0000OOO0}R/{OOOOO0O000O00O000}T)")#line:413:info_label.config(text=f"time range:[{start}~{end}],MP9 overall retest :{failrate} ({fail}R/{input}T)")
def process_data ():#line:416:def process_data():
    info_label .config (text ="")#line:417:info_label.config(text="")
    if not input_path :#line:418:if not input_path:
        info_label .config (text ="input folder not selected！")#line:419:info_label.config(text="input folder not selected！")
        return #line:420:return
    if not output_path :#line:421:if not output_path:
        info_label .config (text ="output folder not selected！")#line:422:info_label.config(text="output folder not selected！")
        return #line:423:return
    create_folder ()#line:424:create_folder()
    OOOOO0OOO0OOOOOOO =var0 .get ()#line:425:select_station = var0.get()
    if OOOOO0OOO0OOOOOOO =='TSP':#line:426:if select_station == 'TSP':
        process_tsp_data ()#line:427:process_tsp_data()
    elif OOOOO0OOO0OOOOOOO =='DVA':#line:428:elif select_station == 'DVA':
        process_dva_data ()#line:429:process_dva_data()
    elif OOOOO0OOO0OOOOOOO =='MP9':#line:430:elif select_station == 'MP9':
        process_mp9_data ()#line:431:process_mp9_data()
def add_to_16 (OOOOO0O000O0000O0 ):#line:434:def add_to_16(value):
    while len (OOOOO0O000O0000O0 )%16 !=0 :#line:435:while len(value) % 16 != 0:
        OOOOO0O000O0000O0 +='\0'#line:436:value += '\0'
    return str .encode (OOOOO0O000O0000O0 )#line:437:return str.encode(value)
def encrypt (OO0OO0OOO000000O0 ):#line:440:def encrypt(text):
    O00000OOOO000O000 =add_to_16 (OO0OO0OOO000000O0 )#line:441:padded_data = add_to_16(text)
    OO00O000O0O0O00OO =b"pro@chad"#line:443:key = b"pro@chad"
    O0O0OO0OO000OOOO0 =DES .new (OO00O000O0O0O00OO ,DES .MODE_ECB )#line:444:des = DES.new(key, DES.MODE_ECB)
    OOOO000O0OO0O0O00 =O0O0OO0OO000OOOO0 .encrypt (O00000OOOO000O000 )#line:447:encrypted_data = des.encrypt(padded_data)
    O00OO0OOO0O0OO0O0 =base64 .b64encode (OOOO000O0OO0O0O00 ).decode ('utf-8')#line:450:encrypted_hex = base64.b64encode(encrypted_data).decode('utf-8')
    return O00OO0OOO0O0OO0O0 #line:451:return encrypted_hex
def decrypt (O0O0O0000000O0O00 ):#line:454:def decrypt(encrypted_hex):
    O000OOO0000O0OOO0 =b"pro@chad"#line:455:key = b"pro@chad"
    O0O0OOOOOOOOO0O00 =DES .new (O000OOO0000O0OOO0 ,DES .MODE_ECB )#line:457:des = DES.new(key, DES.MODE_ECB)
    OO00OO0O0OO0O00O0 =O0O0OOOOOOOOO0O00 .decrypt (base64 .b64decode (O0O0O0000000O0O00 ))#line:460:decrypted_data = des.decrypt(base64.b64decode(encrypted_hex))
    OO00OO00000000OOO =OO00OO0O0OO0O00O0 .decode ('utf-8')#line:463:decrypted_str = decrypted_data.decode('utf-8')
    return OO00OO00000000OOO #line:464:return decrypted_str
def is_overdated ():#line:467:def is_overdated():
    O00O00O000OOO0O00 =datetime .now ()#line:468:now = datetime.now()
    O0O000OOOO0O00OO0 =datetime (2024 ,3 ,1 ,00 ,00 ,00 )#line:469:TRIAL_END_DATE = datetime(2024, 3, 1, 00, 00, 00)
    OOO0OO0OO00O0OOO0 =os .path .join (Path (__file__ ).parent .resolve (),"license.txt")#line:470:license_path = os.path.join(Path(__file__).parent.resolve(), "license.txt")
    if not os .path .exists (OOO0OO0OO00O0OOO0 ):#line:471:if not os.path.exists(license_path):
        return True #line:472:return True
    else :#line:473:else:
        with open (OOO0OO0OO00O0OOO0 ,"rb")as OOOOO00OOO0O00OO0 :#line:474:with open(license_path, "rb") as f:
            O00O0O000OOO00O0O =OOOOO00OOO0O00OO0 .read ()#line:475:encrypted_data = f.read()
        O0O00000OOOOO0OO0 =decrypt (O00O0O000OOO00O0O )#line:477:decrypted_str = decrypt(encrypted_data)
        O0OOOOOO000O00000 =O0O00000OOOOO0OO0 .count ("@@")#line:478:sep_count = decrypted_str.count("@@")
        if O0OOOOOO000O00000 !=5 :#line:479:if sep_count != 5:  # license error
            return True #line:480:return True
        else :#line:481:else:
            O0OO0OO00000OOO00 =O0O00000OOOOO0OO0 .split ("@@")[4 ]#line:482:trial_end_str = decrypted_str.split("@@")[4]
            OOOO0OOO0O000O0O0 =datetime .strptime (O0OO0OO00000OOO00 ,"%Y-%m-%d %H:%M:%S")#line:483:trial_end_date = datetime.strptime(trial_end_str, "%Y-%m-%d %H:%M:%S")
            if O00O00O000OOO0O00 >OOOO0OOO0O000O0O0 :#line:484:if now > trial_end_date:  # 过期
                return True #line:485:return True
            else :#line:486:else:
                O00OOOOOO0O0OOOOO =O0O00000OOOOO0OO0 .split ("@@")[1 ]#line:487:lldate_str = decrypted_str.split("@@")[1]
                OO000000OO0OOO0OO =datetime .strptime (O00OOOOOO0O0OOOOO ,"%Y-%m-%d %H:%M:%S")#line:488:lldate = datetime.strptime(lldate_str, "%Y-%m-%d %H:%M:%S")
                O00O0OO00O0O0O0O0 =O0O00000OOOOO0OO0 .split ("@@")[3 ]#line:489:lastdate_str = decrypted_str.split("@@")[3]
                OOO00OO00OO000000 =datetime .strptime (O00O0OO00O0O0O0O0 ,"%Y-%m-%d %H:%M:%S")#line:490:lastdate = datetime.strptime(lastdate_str, "%Y-%m-%d %H:%M:%S")
                if OO000000OO0OOO0OO >OOO00OO00OO000000 :#line:491:if lldate > lastdate:  # lldate>lastdate
                    return True #line:492:return True
                else :#line:493:else:
                    O00OOOOOO0O0OOOOO =O00O0OO00O0O0O0O0 #line:494:lldate_str = lastdate_str
                    O00O0OO00O0O0O0O0 =O00O00O000OOO0O00 .strftime ("%Y-%m-%d %H:%M:%S")#line:495:lastdate_str = now.strftime("%Y-%m-%d %H:%M:%S")
                    OOO0OO0O00OOO00O0 =f"T%TRIAL_END_DATE%:@@{O00OOOOOO0O0OOOOO}@@,this date=@@{O00O0OO00O0O0O0O0}@@{O0OO0OO00000OOO00}@@%TRIAL_END_DATE%T"#line:496:content = f"T%TRIAL_END_DATE%:@@{lldate_str}@@,this date=@@{lastdate_str}@@{trial_end_str}@@%TRIAL_END_DATE%T"
                    with open (OOO0OO0OO00O0OOO0 ,"w")as OOOOO00OOO0O00OO0 :#line:498:with open(license_path, "w") as f:
                        OOOOO00OOO0O00OO0 .write (encrypt (OOO0OO0O00OOO00O0 ))#line:499:f.write(encrypt(content))
                    return False #line:500:return False
def insert_text (O000O0O000O0O0O0O ):#line:503:def insert_text(local_):
    local_file .config (state ='normal',bg ='#303030',fg ='white')#line:504:local_file.config(state='normal', bg='#303030', fg='white')
    local_file .insert (1.0 ,O000O0O000O0O0O0O +'\n')#line:505:local_file.insert(1.0, local_ + '\n')
    local_file .config (state ='disabled',bg ='#303030',fg ='white')#line:506:local_file.config(state='disabled', bg='#303030', fg='white')
def start_thread ():#line:509:def start_thread():
    O00OO000OOO00000O =threading .Thread (target =process_data )#line:510:t = threading.Thread(target=process_data)
    O00OO000OOO00000O .start ()#line:511:t.start()
root =Tk ()#line:514:root = Tk()
if is_overdated ():#line:515:if is_overdated():
    root .withdraw ()#line:516:root.withdraw()
    messagebox .showinfo ("hint","license expired！")#line:517:messagebox.showinfo("hint", "license expired！")
root .geometry ("900x300+100+100")#line:518:root.geometry("900x300+100+100")
root .title ("Data analyzer")#line:519:root.title("Data analyzer")
input_label =Label (root ,width =24 ,text ="please select the input folder  ")#line:520:input_label = Label(root, width=24, text="please select the input folder  ")
input_label .grid (row =1 ,column =1 ,columnspan =3 ,sticky ='w')#line:521:input_label.grid(row=1, column=1, columnspan=3, sticky='w')
input_button =Button (root ,text ="input csv folder",command =select_csv_file )#line:522:input_button = Button(root, text="input csv folder", command=select_csv_file)
input_button .grid (row =1 ,column =0 ,sticky ='ew')#line:523:input_button.grid(row=1, column=0, sticky='ew')
input_path =""#line:524:input_path = ""
output_label =Label (root ,width =24 ,text ="please select the output folder")#line:526:output_label = Label(root, width=24, text="please select the output folder")
output_label .grid (row =2 ,column =1 ,columnspan =3 ,sticky ='w')#line:527:output_label.grid(row=2, column=1, columnspan=3, sticky='w')
output_button =Button (root ,text ="output folder",command =select_output_path )#line:528:output_button = Button(root, text="output folder", command=select_output_path)
output_button .grid (row =2 ,column =0 ,sticky ='ew')#line:529:output_button.grid(row=2, column=0, sticky='ew')
output_path =""#line:530:output_path = ""
process_button =Button (root ,text ="process data",command =start_thread )#line:532:process_button = Button(root, text="process data", command=start_thread)
process_button .grid (row =3 ,column =0 ,sticky ='ew')#line:533:process_button.grid(row=3, column=0, sticky='ew')
radio_frame =Frame (root )#line:535:radio_frame = Frame(root)
radio_frame .grid (row =3 ,column =1 )#line:536:radio_frame.grid(row=3, column=1)
var0 =StringVar ()#line:537:var0 = StringVar()
radio1 =Radiobutton (radio_frame ,text ="TSP",value ="TSP",variable =var0 )#line:538:radio1 = Radiobutton(radio_frame, text="TSP", value="TSP", variable=var0)
radio1 .grid (row =0 ,column =0 ,sticky ='w')#line:539:radio1.grid(row=0, column=0, sticky='w')
radio2 =Radiobutton (radio_frame ,text ="DVA",value ="DVA",variable =var0 )#line:540:radio2 = Radiobutton(radio_frame, text="DVA", value="DVA", variable=var0)
radio2 .grid (row =0 ,column =1 ,sticky ='w')#line:541:radio2.grid(row=0, column=1, sticky='w')
radio3 =Radiobutton (radio_frame ,text ="MP9",value ="MP9",variable =var0 )#line:542:radio3 = Radiobutton(radio_frame, text="MP9", value="MP9", variable=var0)
radio3 .grid (row =0 ,column =2 ,sticky ='w')#line:543:radio3.grid(row=0, column=2, sticky='w')
var0 .set ('TSP')#line:544:var0.set('TSP')
info_label =Label (root ,text =" ")#line:546:info_label = Label(root, text=" ")
info_label .grid (row =9 ,column =0 ,columnspan =5 )#line:547:info_label.grid(row=9, column=0, columnspan=5)
local_file =Text (root ,width =125 ,height =14 )#line:549:local_file = Text(root, width=125, height=14)
local_file .config (state ='disabled',bg ='#303030',fg ='white')#line:550:local_file.config(state='disabled', bg='#303030', fg='white')
local_file .grid (row =10 ,column =0 ,columnspan =5 )#line:551:local_file.grid(row=10, column=0, columnspan=5)
root .protocol ("WM_DELETE_WINDOW",on_closing )#line:553:root.protocol("WM_DELETE_WINDOW", on_closing)
root .mainloop ()#line:554:root.mainloop()
