import datetime
import pymysql
import pandas as pd
import time
import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
import get_code

# 시작시간
start_time = time.time()
# today
now = datetime.datetime.now()
today = now.strftime("%Y.%m.%d")

# mysql connecting info & connect
key_df = pd.read_csv('../aws_db_key.txt', header=None)
host, user, password, db = key_df[0][0], key_df[0][1], key_df[0][2], key_df[0][3]
conn = pymysql.connect(host=host, user=user, password=password, db=db)
curs = conn.cursor()

# get code
get_code.from_xls(conn)

def txt2int(txt):
    txt_sub = re.sub(',', '', txt)
    p = re.compile('[\-\d]+')  # 음수부호 포함
    n_li = p.findall(txt_sub)
    result = ''
    for n_txt in n_li:  # 예) '41조 970억' -> 410970
        result += n_txt.zfill(4)
    return int(result)


# 종목별 오늘 시황 업데이트
def stock_crawling(code):
    # print(code)

    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    dfs = pd.read_html(url, encoding='euc-kr')  # 페이지 내 모든 테이블 (3:분석실적 -8:시가총액, -6:52주최고, -4:동일업종)

    # 종목명
    name = soup.select_one("div.wrap_company h2").text

    # 마켓(코스피, 코스닥), 업종 크롤링
    market_code = soup.select_one("div.description img")['class'][0].upper()  # 마켓
    cat_id = int(soup.select("div#tab_con1 th a.link_site")[-1]['href'].split("=")[-1])  # 업종 id
    category = globals()['cat_df'][globals()['cat_df']['ID'] == cat_id]['Category'].values[0]  # 업종

    # 시가총액, 52주 최고가
    capital = txt2int(dfs[-8].iloc[0, 1])  # 시가총액
    highest_price = txt2int(dfs[-6].iloc[1, 1].split()[0])  # 52주 최고가

    # 기업분석실적
    df = dfs[3].set_index(dfs[3].columns[0])

    per = df.loc['PER(배)'][-2]
    eps = df.loc['EPS(원)'][-2]
    roe = df.loc['ROE(지배주주)'][-2]
    pbr = df.loc['PBR(배)'][-2]
    bps = df.loc['BPS(원)'][-2]
    group_per = float(dfs[-4].loc[0,1][:-1])  # 동일업종 PER(배)

    revenue = df.loc['매출액'][-2]
    operating_income = df.loc['영업이익'][-2]
    net_income = df.loc['당기순이익'][-2]
    dividend = df.loc['시가배당률(%)'][2]

    debt = df.loc['부채비율'][-2]
    debts, debt_continuous = df.loc['부채비율'][-6:-1], 1  # 부채가 몇년 연속 줄었는가
    for i in range(1,5):
        if float(debts[-i]) < float(debts[-i-1]):
            debt_continuous += 1
        else:
            break

    retention = df.loc['유보율'][-2]
    retentions, retention_continuous = df.loc['유보율'][-6:-1], 1  # 유보율이 몇년 연속 늘었는가
    for i in range(1,5):
        if float(retentions[-i]) >= float(retentions[-i-1]):
            retention_continuous += 1
        else:
            break

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

    # 52주 최고가일
    curs.execute(f"""SELECT Date, High FROM stocksearch.past_market where id = "{code}"
                and High = (SELECT max(High) FROM stocksearch.past_market where id = "{code}") Order by Date DESC;""")
    ex_highest = curs.fetchone()
    if high >= ex_highest[1]:
        highest_date = today
    else:
        highest_date = ex_highest[0].strftime("%Y.%m.%d")


    # null값('-' -> 0, nan -> null) 처리
    values_li = [per,  eps,  roe,  pbr,  bps,  revenue,  operating_income,  net_income, dividend]
    if '-' in values_li:
        for idx, val in enumerate(values_li):
            if val == '-':
                values_li[idx] = 0
    if True in (pd.isna([values_li])):
        for idx, val in enumerate(values_li):
            if pd.isna(val):
                values_li[idx] = 'NULL'
    per, eps, roe, pbr, bps, revenue, operating_income, net_income, dividend = values_li

    # daily_market 업데이트
    update_sql_1 = f"""UPDATE stocksearch.daily_market
                    SET Name = "{name}", Market = "{market_code}", Category="{category}", Capital = {capital},
                    PER = {per}, EPS = {eps}, ROE = {roe}, PBR = {pbr}, BPS = {bps}, Group_PER = {group_per},
                    Revenue = {revenue}, Operating_Income = {operating_income}, Net_Income = {net_income}, Dividend = {dividend}, 
                    Debt = {debt}, Debt_continuous = {debt_continuous}, Retention = {retention}, Retention_Continuous = {retention_continuous},
                    Open = {open}, High = {high}, Low = {low}, Close = {close}, Volume = {volume}, DaytoDay = {day2day},
                    Highest_Price = {highest_price}, Highest_Date = "{highest_date}"
                    WHERE ID = "{code}"; """
    curs.execute(update_sql_1)

    # # past_market 업데이트
    update_sql_2 = f"""INSERT INTO stocksearch.past_market
            (ID, Date, Open, High, Low, Close, Volume) Values
            ('{code}', "{today}", {open}, {high}, {low}, {close}, {volume}); """
    curs.execute(update_sql_2)
    conn.commit()

#
# if __name__ == '__main__':
#     # 종목리스트 선출
#     daily_df = pd.read_sql("select * from stocksearch.daily_market", conn)
#     code_li = daily_df['ID']
#
#     # 오늘 장이 열렸었는지 확인
#     code = code_li[0]
#     url = f"https://finance.naver.com/item/main.nhn?code={code}"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     # 장마감 날짜 확인
#     f = soup.select_one("em.date")
#     f.span.decompose()
#     final_day = f.get_text().strip().split()[0]
#     print('today :', today)
#     print('recent open day :', final_day)
#     if today != final_day:
#         print('market is closed today')
#
#     else:
#         # 멀티 쓰레딩 Pool 사용
#         pool = Pool(processes=4)  # 4개의 프로세스를 사용합니다.
#         pool.map(stock_crawling, code_li)  # pool에 일을 던져줍니다.
#         print("--- %s seconds ---" % (time.time() - start_time))


# test
daily_df = pd.read_sql("select * from stocksearch.daily_market", conn)
code_li = daily_df['ID']
globals()['cat_df'] = pd.read_sql("SELECT * FROM stocksearch.category;", conn)
for i in range(1193, len(code_li)):
    code = code_li[i]
    print(i, code)
    stock_crawling(code)


code = "071840"