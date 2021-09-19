import datetime
import pymysql
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import locale


import os
os.chdir('backend')

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
    txt_sub = re.sub(',','',txt)
    p = re.compile('[\-\d]+')  # 음수부호 포함
    num_txt = p.findall(txt_sub)[0]
    n_li = p.findall(num_txt)
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

dfs = pd.read_html(url, encoding='euc-kr')  # 페이지 내 모든 테이블

# 장마감 날짜 확인
f = soup.select_one("em.date")
f.span.decompose()
final_day = f.get_text()
final_day = re.sub('\.','', final_day).strip()

if today != final_day:
    print('오늘 아님')

# 마켓(코스피, 코스닥), 업종 크롤링
market_code = soup.select_one("div.description img")['class'][0]  # 마켓
category = soup.select_one("div.section.trade_compare > h4 > em a").text  # 업종

# 시가총액, 52주 최고가
capital = txt2int(dfs[5].iloc[0, 1])  # 시가총액
highest_price = txt2int(dfs[7].iloc[1, 1].split()[0])  # 52주 최고가
highest_date = ""

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

# 기업분석실적
df = dfs[3].set_index(dfs[3].columns[0])

per = df.loc['PER(배)'][-2]
eps = df.loc['EPS(원)'][-2]
roe = df.loc['ROE(지배주주)'][-2]
pbr = df.loc['PBR(배)'][-2]
bps = df.loc['BPS(원)'][-2]
float(dfs[9].loc[0,1][:-1])  # 동일업종 PER(배)

revenue = df.loc['매출액'][-2]
operating_income = df.loc['영업이익'][-2]
net_income = df.loc['당기순이익'][-2]

df.loc['부채비율'][-2]
df.loc['유보율'][-2]
df.loc['시가배당률(%)'][2]

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






print(cnt, code, close, high, volume, open, low, capital)
cnt += 1


