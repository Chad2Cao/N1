import base64
from datetime import datetime, timedelta
from Crypto.Cipher import DES

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


def generate_license():
    trial_end = datetime.now() + timedelta(days=30)
    trial_end_str = trial_end.strftime("%Y-%m-%d %H:%M:%S")
    lldate = datetime.now() - timedelta(days=1)
    lldate_str = lldate.strftime("%Y-%m-%d %H:%M:%S")
    lastdate_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"T%TRIAL_END_DATE%:@@{lldate_str}@@,this date=@@{lastdate_str}@@{trial_end_str}@@%TRIAL_END_DATE%T"
    with open("license.txt", "w") as f:
        f.write(encrypt(content))

generate_license()