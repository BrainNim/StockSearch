import daily_update
import get_year_data
import time
from get_data import get_code

# daily_update.update(start_num=0)
get_code.from_xlsx()


i = 0

if i == 0:
    # daily_update.update(start_num=0)
    get_year_data.update(start_num=0, del_chk=True)
else:
    # daily_update.update(start_num=i*1000)
    get_year_data.update(start_num=i*1000)
