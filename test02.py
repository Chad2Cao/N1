from datetime import datetime,timedelta

def get_date_list():
    selected = '一周'
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
    combined_str_list = [[date.strftime('%Y-%m-%d'), date.strftime('%Y%m%d')] for date in date_list]
    return combined_str_list

def test_for_loop(date_comp_):
    if date_comp_ in [['2024-02-26', '20240226'], ['2024-02-25', '20240225']]:
        return
    else:
        print(date_comp_)

for date_comp in get_date_list():
    test_for_loop(date_comp)
