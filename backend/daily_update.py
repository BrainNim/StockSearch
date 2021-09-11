from pykiwoom.kiwoom import *
import datetime
import pymysql
import pandas as pd
import time

def update(start_num = 0):
    start_num = 0

    # today
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")
    print(today)

    # Login
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)
    print('로그인 성공')

    # mysql connecting info & connect
    key_df = pd.read_csv('aws_db_key.txt', header=None)
    host, user, password, db = key_df[0][0], key_df[0][1], key_df[0][2], key_df[0][3]
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    curs = conn.cursor()
    yesterday_df = pd.read_sql("select * from stocksearch.daily_market", conn)


    # get_code_list_by_market (펀드, etf제거)
    kospi_code = kiwoom.GetCodeListByMarket('0')
    kosdaq_code = kiwoom.GetCodeListByMarket('10')
    mutual_code = kiwoom.GetCodeListByMarket('4')
    etf_code = kiwoom.GetCodeListByMarket('8')

    total_code = (set(kosdaq_code) | set(kospi_code)) - (set(mutual_code) | set(etf_code))
    total_code = list(total_code)

    market_code = []
    for code in total_code:
        if code in kospi_code:
            market_code.append('KOSPI')
        elif code in kosdaq_code:
            market_code.append('KOSDAQ')

    print("총 종목 수 :", len(total_code), '(ETN 종목 포함)')


    # 기존 종목 리스트와 다른 점이 있다면 종목 추가/수정
    if len(total_code) != len(yesterday_df):
        new_code = list(set(total_code) - set(yesterday_df['ID']))
        del_code = list(set(yesterday_df['ID']) - set(total_code))

        if len(new_code) > 0:
            for code in new_code:
                curs.execute(f"INSERT INTO stocksearch.daily_market (ID) VALUES ('{code}')")
            conn.commit()
            print(len(new_code), '개 신규종목 추가')

        if len(del_code) > 0:  # 추후 데이터에서 제거하는 것이 아닌 IS_ENABLE을 추가, 변경
            for code in del_code:
                curs.execute(f"DELETE FROM stocksearch.daily_market WHERE ID = '{code}'")
            conn.commit()
            print(len(del_code), '개 폐지종목 제거')


    # 종목별 오늘 시황 업데이트
    daily_df = pd.read_sql("select * from stocksearch.daily_market", conn)
    code_li = daily_df['ID']

    print('조회제한 방지 위해 10초 휴식중...')
    time.sleep(10)
    for i in range(start_num, len(code_li)):
        code = code_li[i]
        print(f"{code} ({i}/{len(code_li)})")
        time.sleep(0.6)
        today_df = kiwoom.block_request("opt10001",
                                        종목코드=code,
                                        기준일자=today,
                                        수정주가구분=1,
                                        output="주식기본정보요청",
                                        next=0)
        today_df = today_df.iloc[0]
        today_df[today_df.isin([""])] = 'NULL'  # 결측치 처리

        # ETN 종목 제거
        if 'ETN' in today_df['종목명']:
            curs.execute(f"DELETE FROM stocksearch.daily_market WHERE ID = '{code}'")
            conn.commit()
            print(f"{code} ({i}/{len(code_li)}) 제거 - 사유: ETN 종목")

            continue

        # daily_market 업데이트
        update_sql_1 = f"""UPDATE stocksearch.daily_market
                        SET Name = "{today_df['종목명']}", Market = "{market_code[i]}", Capital = {today_df['시가총액']},
                        PER = {today_df['PER']}, EPS = {today_df['EPS']}, ROE = {today_df['ROE']},
                        PBR = {today_df['PBR']}, EV = {today_df['EV']}, BPS = {today_df['BPS']},
                        Revenue = {today_df['매출액']}, Operating_Income = {today_df['영업이익']}, Net_Income = {today_df['당기순이익']},
                        Open = {abs(int(today_df['시가']))}, High = {abs(int(today_df['고가']))}, Low = {abs(int(today_df['저가']))},
                        Close = {abs(int(today_df['현재가']))}, Volume = {abs(int(today_df['거래량']))}, DaytoDay = {float(today_df['전일대비'])},
                        Highest_Price = {abs(int(today_df['250최고']))}, Highest_Date = {today_df['250최고가일']}
                        WHERE ID = '{code}'; """
        curs.execute(update_sql_1)
        conn.commit()

        # past_market 업데이트
        update_sql_2 = f"""INSERT INTO stocksearch.past_market
                (ID, Date, Open, High, Low, Close, Volume) Values
                ('{code}', {today}, {abs(int(today_df['시가']))}, {abs(int(today_df['고가']))},
                {abs(int(today_df['저가']))}, {abs(int(today_df['현재가']))}, {abs(int(today_df['거래량']))}); """
        curs.execute(update_sql_2)
        conn.commit()

        # if i % 1000 == 999:  # 1000개마다 60초 휴식
        #     print('조회제한 방지 위해 60초 휴식 후 재로그인')
        #     kiwoom.CommConnect(block=True)
        #     time.sleep(60)

    conn.close()