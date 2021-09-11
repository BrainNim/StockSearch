import daily_update
import get_year_data
import time

# daily_update.update(start_num=0)

for i in range(2,3):
    if i == 0:
        print('10초 휴식')
        time.sleep(10)
        get_year_data.update(start_num=0, del_chk=True)
    else:
        print('10초 휴식')
        time.sleep(10)
        get_year_data.update(start_num=i*1000)
