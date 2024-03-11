import csv

list_of_dict=[]
# 打开csv文件
with open('/Users/chad/PycharmProjects/TSP/spec_for_tsp_e.csv', 'r', encoding='utf-8') as csvfile:
    # 创建csv阅读器对象
    csv_reader = csv.reader(csvfile)
    next(csv_reader)
    # 遍历csv文件的每一行
    for row in csv_reader:
        end = 8
        for i in range(2, 8):
            if row[i] == "":
                end = i
                # print(i,end='')
                break
        key = '_'.join(row[0:end])
        spec = f'[{row[8]}~{row[9]}]'
        my_dict = {'key': key, 'spec': spec}
        list_of_dict.append(my_dict)

with open('key_for_spec.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list_of_dict[0].keys())

    # 写入表头
    writer.writeheader()

    # 写入数据
    for row in list_of_dict:
        writer.writerow(row)
# print(key, spec, probe)
