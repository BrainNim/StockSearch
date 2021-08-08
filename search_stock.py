import time
import pymysql
import pandas as pd
from search_filter import *
from sqlalchemy import create_engine

# connect mysql
conn = pymysql.connect(host="localhost",
                       user="root",
                       password="0000",
                       db="stocksearch")
# curs = conn.cursor()

start = time.time()

df = pd.read_sql("select * from stocksearch.daily_market", conn)

CrossFilter(conn).goldencross(5, 20, df)

# 필터 0
df0 = MarketFilter.market("KOSPI", df)

# 필터 1
df1 = PriceFilter(conn).updown(1000, 100000, df0)

# 필터 2
df2 = PriceFilter(conn).compare_mean(365, 1.1, 'up', df1)

# 필터 3
df3 = PriceFilter(conn).compare_max(0.5, df2)

# 필터 4
df4 = PERFilter.top('top', 20, df3)

print(time.time() -start)


start = time.time()
df = pd.read_sql("select * from stocksearch.daily_market", conn)
VolumeFilter.compare_max(0.7, df, conn)
print(time.time() -start)


conn.close()