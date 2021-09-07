import json
import pymysql
import pandas as pd
from flask import Flask, request
from search_filter import *
from collections import Counter

# Flask
app = Flask(__name__)


###### SEARCH FILTER #####
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI
# http://127.0.0.1:5000/?PriceFilter.dist_max=60,in
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.compare_max=0.7
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.updown=1000,10000&PriceFilter.compare_max=0.7
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.updown=1000,10000&PriceFilter.compare_max=0.7&CrossFilter.goldencross=5,20
@app.route('/', methods=['GET', ])
def filter():
    # mysql connecting info & connect
    key_df = pd.read_csv('aws_db_key.txt', header=None)
    host, user, password, db = key_df[0][0], key_df[0][1], key_df[0][2], key_df[0][3]
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    curs = conn.cursor()

    df = pd.read_sql("select * from stocksearch.daily_market", conn)

    # read query & parameters
    query = request.query_string.decode('utf-8')
    parameters = query.split('&')

    if len(parameters) == 0:
        return df.ID.to_string()

    # data filtering
    for param in parameters:
        func = param.split('=')[0].split('.')[0]
        method = param.split('=')[0].split('.')[-1]
        values = param.split('=')[-1].split(',')
        filter_func = getattr(globals()[func](conn), method)
        df = filter_func(*values, df)

    # result에 필요한 칼럼 정보
    cols = ['Name', 'ID', 'Close', 'Volume', 'DaytoDay']
    df = df[cols]

    # one_year_before에 필요한 칼럼 정보
    ids = df.ID.to_list()
    one_year_ago_date_sql = "SELECT Date FROM stocksearch.past_market WHERE Date <= date_add(now(), interval -1 year) GROUP BY Date ORDER BY Date DESC LIMIT 1;"  # 1년 전 날짜
    curs.execute(one_year_ago_date_sql)
    one_year_ago_date = curs.fetchone()[0]
    one_year_ago_date = one_year_ago_date.strftime("%Y-%m-%d")

    where_str = ''
    for id in ids:
        where_str += f'ID = "{id}" or '
    where_str = where_str[:-3]  # 마지막 'or ' 제거
    one_year_ago_sql = f"""SELECT ID, Close FROM stocksearch.past_market 
                        WHERE Date = "{one_year_ago_date}"
                        and ({where_str});"""
    one_year_ago_df = pd.read_sql(one_year_ago_sql, conn)
    new_df = pd.merge(one_year_ago_df, df, left_on='ID', right_on='ID', how='inner')
    one_year_ago_df['rate'] = new_df.apply(lambda x: (x.Close_y - x.Close_x) / x.Close_x * 100, axis=1)

    answer = {}
    answer['result'] = df.to_dict('records')
    answer['one_year_before_date'] = one_year_ago_date
    answer['one_year_before'] = one_year_ago_df.to_dict('records')

    # 요청 log를 DB에 저장
    save_request_log(query, curs, conn)

    return json.dumps(answer, ensure_ascii=False, indent=4)


###### DICTIONARY #####
# http://127.0.0.1:5000/dictionary
# http://127.0.0.1:5000/dictionary/2
@app.route('/dictionary/', methods=['GET', ])
@app.route('/dictionary/<int:Dic_SN>', methods=['GET', ])
def dic(Dic_SN=None):
    # mysql connecting info & connect
    key_df = pd.read_csv('aws_db_key.txt', header=None)
    host, user, password, db = key_df[0][0], key_df[0][1], key_df[0][2], key_df[0][3]
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    curs = conn.cursor()

    if Dic_SN == None:
        total_df = pd.read_sql("SELECT Dic_SN, Title FROM stocksearch.dictionary;", conn)
        answer = total_df.to_dict('records')

    else:
        curs.execute(f"SELECT * FROM stocksearch.dictionary WHERE Dic_SN = {Dic_SN};")
        dic_data = curs.fetchone()
        answer = dict(zip(['Dic_SN', 'Title', 'Description', 'Condition'], dic_data))
        print(answer)

    return json.dumps(answer, ensure_ascii=False, indent=4)


###### Board #####
# 유저가 searchfilter를 사용할 때 마다 요청쿼리를 저장
def save_request_log(request, curs, conn):
    sql = f"INSERT INTO stocksearch.request_history (query) VALUES ('{request}')"
    curs.execute(sql)
    conn.commit()


# 전체쿼리문 -> 필터명 전처리 함수
def proc_query(query):
    query_li = query.split('&')
    proc_str = ''
    for q in query_li:
        f = q.split('=')[0]
        proc_str += f+','
    return proc_str


# http://127.0.0.1:5000/board
@app.route('/board/', methods=['GET', ])
def board():
    # mysql connecting info & connect
    key_df = pd.read_csv('aws_db_key.txt', header=None)
    host, user, password, db = key_df[0][0], key_df[0][1], key_df[0][2], key_df[0][3]
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    curs = conn.cursor()

    sql = "SELECT Query FROM stocksearch.request_history;"
    board_df = pd.read_sql(sql, conn)
    # 사용한 필터 수가 2개 이상인 경우에만 살림
    board_df['filter_count'] = board_df.Query.apply(lambda x: len(x.split('&')))
    board_df = board_df[board_df['filter_count'] >= 2]

    # 값을 제거하고 이용한 필터만 뽑아내기
    board_df['filter_ori'] = board_df.Query.apply(lambda x: proc_query(x))
    # 각 필터조합 당 수 세기
    query_count = Counter(list(board_df.filter_ori))

    board_df['duplicated_count'] = 0

    # for filter_ori in query_count:
    #     board_df['duplicated_count']
    #     print(filter_ori, query_count[filter_ori])

    return board_df.to_json(orient='index')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
