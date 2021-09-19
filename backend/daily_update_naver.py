import datetime
import pymysql
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
# import locale

# today
import re
now = datetime.datetime.now()
today = now.strftime("%Y%m%d")
print(today)

# mysql connecting info & connect
key_df = pd.read_csv('aws_db_key.txt', header=None)
host, user, password, db = key_df[0][0], key_df[0][1], key_df[0][2], key_df[0][3]
conn = pymysql.connect(host=host, user=user, password=password, db=db)
curs = conn.cursor()
yesterday_df = pd.read_sql("select * from stocksearch.daily_market", conn)

# get_code_list_by_market
# kospi_code = kiwoom.GetCodeListByMarket('0')
# kosdaq_code = kiwoom.GetCodeListByMarket('10')
# total_code = kospi_code + kosdaq_code

# print("총 종목 수 :", len(total_code))

# 기존 종목 리스트와 다른 점이 있다면 종목 추가/수정
# if len(total_code) != len(yesterday_df):
#     new_code = list(set(total_code) - set(yesterday_df['ID']))
#     del_code = list(set(yesterday_df['ID']) - set(total_code))
#
#     if len(new_code) > 0:
#         for code in new_code:
#             curs.execute(f"INSERT INTO stocksearch.daily_market (ID) VALUES ('{code}')")
#         conn.commit()
#         print(len(new_code), '개 신규종목 추가')
#
#     if len(del_code) > 0:  # 추후 데이터에서 제거하는 것이 아닌 IS_ENABLE을 추가, 변경
#         for code in del_code:
#             curs.execute(f"DELETE FROM stocksearch.daily_market WHERE ID = '{code}'")
#         conn.commit()
#         print(len(del_code), '개 폐지종목 제거')

# 텍스트 - 숫자 전환용
# locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

def txt2int(txt):
    txt = re.sub(',', '', txt)
    p = re.compile('\d+')
    n_li = p.findall(txt)
    result = ''
    for n_txt in n_li:  # 예) '41조 970억' -> 410970
        result += n_txt.zfill(4)
    return int(result)

# 종목별 오늘 시황 업데이트
daily_df = pd.read_sql("select * from stocksearch.daily_market", conn)
code_li = daily_df['ID']

cnt = 0
# for code in code_li:
code = code_li[0]
url = f"https://finance.naver.com/item/main.nhn?code={code}"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# 가격 크롤링
price_soup = soup.select("div.today p.no_today em span")
price_other_soup = soup.select("table.no_info tr td")
close = txt2int(price_soup[0].get_text())  # 현재가, 종가
high = txt2int(price_other_soup[1].em.span.get_text())  # 고가
volume = txt2int(price_other_soup[2].em.span.get_text())  # 거래량
open = txt2int(price_other_soup[3].em.span.get_text())  # 시가
low = txt2int(price_other_soup[4].em.span.get_text())  # 저가

# 전일대비 가격변동
exday_soup = soup.select("div.today p.no_exday em span")
if exday_soup[0].get_text() == '하락':
    day2day = - txt2int(exday_soup[1].get_text())
else:
    day2day = txt2int(exday_soup[1].get_text())

# 상세정보
detail_soup = soup.select("div.aside_invest_info > div.tab_con1 table")
capital = txt2int(detail_soup[0].em.get_text())  # 시가총액

# 기업분석실적
perform_df = soup.select("div.section.cop_analysis")


print(cnt, code, close, high, volume, open, low, capital)
cnt += 1


