import pymysql
import pandas as pd


def from_xlsx():
    # mysql connecting info & connect
    key_df = pd.read_csv('aws_db_key.txt', header=None)
    host, user, password, db = key_df[0][0], key_df[0][1], key_df[0][2], key_df[0][3]
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    curs = conn.cursor()

    yesterday_df = pd.read_sql("select ID from stocksearch.daily_market", conn)

    # today total code
    # http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101 에서 엑셀파일 다운로드
    kospi_df = pd.read_excel('get_data/KOSPI.xlsx', dtype='object')
    kosdaq_df = pd.read_excel('get_data/KOSDAQ.xlsx', dtype='object')

    # delete SPAC
    kosdaq_df = kosdaq_df[kosdaq_df['소속부'] != 'SPAC(소속부없음)']

    # total_code = list(kospi_df['종목코드']) + list(kosdaq_df['종목코드'])
    # total_name = list(kospi_df['종목명']) + list(kosdaq_df['종목명'])

    total_df = pd.concat([kospi_df, kosdaq_df])

    # 기존 종목 리스트와 다른 점이 있다면 종목 추가/수정
    if len(total_df) != len(yesterday_df):
        new_code = list(set(total_df['종목코드']) - set(yesterday_df['ID']))
        del_code = list(set(yesterday_df['ID']) - set(total_df['종목코드']))

        if len(new_code) > 0:
            for code in new_code:
                name = total_df[total_df['종목코드'] == code]['종목명'].values[0]
                curs.execute(f"INSERT INTO stocksearch.daily_market (ID) VALUES ('{code}')")

            conn.commit()
            print('Insert :', len(new_code))

        if len(del_code) > 0:
            for code in del_code:
                curs.execute(f"DELETE FROM stocksearch.daily_market WHERE ID = '{code}'")
            conn.commit()
            print('Delete :', len(del_code))

    # 종목명 update
    for code, name in zip(total_df['종목코드'], total_df['종목명']):
        curs.execute(f"UPDATE stocksearch.daily_market SET Name = '{name}' WHERE ID = '{code}'")

    conn.commit()
