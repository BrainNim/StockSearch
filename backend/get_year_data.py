import pymysql
import datetime
import pandas as pd
from pykiwoom.kiwoom import *

start_num = 0

# 오늘날짜
now = datetime.datetime.now()
today = now.strftime("%Y%m%d")

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
print('로그인 성공')

# connect mysql
conn = pymysql.connect(host="localhost",
                       user="root",
                       password="0000",
                       db="stocksearch")
curs = conn.cursor()

# past_market 테이블 리셋
# print("past_market 테이블 리셋중...")
# curs.execute("DELETE FROM stocksearch.past_market")
# conn.commit()
# print("리셋완료")

code_df = pd.read_sql("select ID from stocksearch.daily_market", conn)


for idx in range(start_num, len(code_df)):
    code = code_df['ID'].iloc[idx]
    time.sleep(0.4)
    print(idx, code)
    # 약 2년치 요청
    df = kiwoom.block_request("opt10081",
                              종목코드=code,
                              기준일자=today,
                              수정주가구분=1,
                              output="주식일봉차트조회",
                              next=0)

    df = df[['일자', '시가', '고가', '저가', '현재가', '거래량']]
    col = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df.columns = col

    for i in range(len(df)):
        sql = f"""INSERT INTO stocksearch.past_market
                (ID, Date, Open, High, Low, Close, Volume) Values 
                ('{code}', {df['Date'].iloc[i]}, {df['Open'].iloc[i]}, {df['High'].iloc[i]}, 
                {df['Low'].iloc[i]}, {df['Close'].iloc[i]}, {df['Volume'].iloc[i]}) ; """
        curs.execute(sql)
    conn.commit()

conn.close()

