import pymysql
import pandas as pd


def from_xls(conn):
    # mysql connecting info & connect
    curs = conn.cursor()
    yesterday_df = pd.read_sql("select ID from stocksearch.daily_market", conn)

    # today total code
    kospi_df = pd.read_html('KOSPI.xls', converters={'종목코드': str})[0]
    kosdaq_df = pd.read_html('KOSDAQ.xls', converters={'종목코드': str})[0]
    total_code = list(kospi_df['종목코드']) + list(kosdaq_df['종목코드'])

    # 기존 종목 리스트와 다른 점이 있다면 종목 추가/수정
    if len(total_code) != len(yesterday_df):
        new_code = list(set(total_code) - set(yesterday_df['ID']))
        del_code = list(set(yesterday_df['ID']) - set(total_code))

        if len(new_code) > 0:
            for code in new_code:
                curs.execute(f"INSERT INTO stocksearch.daily_market (ID) VALUES ('{code}')")
            conn.commit()
            print('Insert :', len(new_code))

        if len(del_code) > 0:
            for code in del_code:
                curs.execute(f"DELETE FROM stocksearch.daily_market WHERE ID = '{code}'")
            conn.commit()
            print('Delete :', len(del_code))
