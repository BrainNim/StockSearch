import json
import time
import pymysql
import pandas as pd
from flask import Flask, request
from search_filter import *
from collections import Counter
pd.set_option('display.max_columns', None)
# Flask
app = Flask(__name__)


###### CONNECT DB ######
def connect_db():
    # mysql connecting info & connect
    key_df = pd.read_csv('aws_db_key.txt', header=None)
    host, user, password, db = key_df[0][0], key_df[0][1], key_df[0][2], key_df[0][3]
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    curs = conn.cursor()
    return conn, curs


###### FILTER LIST #####
# http://127.0.0.1:5000/filter_li
# http://127.0.0.1:5000/filter_li/2
@app.route('/filter_li/', methods=['GET', ])
@app.route('/filter_li/<int:Filter_SN>', methods=['GET', ])
def filter_li(Filter_SN=None):
    # mysql connecting info & connect
    conn, curs = connect_db()

    if Filter_SN == None:
        df = pd.read_sql("SELECT FL_SN, Filter, Filter_KOR, Subfilter, Subfilter_KOR FROM stocksearch.filter_list;", conn)

        df['subfilter'] = df.apply(lambda x: {'filter_SN': x['FL_SN'], 'name': x['Subfilter'], 'kor_name': x['Subfilter_KOR']}, axis=1)
        df = df.drop(['FL_SN', 'Subfilter', 'Subfilter_KOR'], axis=1)

        main_filter = df.drop_duplicates('Filter')
        result = []
        for i in range(len(main_filter)):
            name, kor_name = main_filter.iloc[i].Filter, main_filter.iloc[i].Filter_KOR
            f_dict = {'name': name, 'kor_name': kor_name}
            sub_li = []
            for sub in df[df['Filter'] == name].subfilter:
                sub_li.append(sub)
            f_dict['subfilter'] = sub_li
            result.append(f_dict)

        result = {'filter': result}

    else:
        df = pd.read_sql(f"SELECT * FROM stocksearch.filter_list WHERE FL_SN = {Filter_SN};", conn)
        df['input'] = df.apply(lambda x: {'type': x['input_type'], 'data_format': x['input_format']}, axis=1)
        df['user_view'] = df.apply(
            lambda x: {'description': x['description'], 'default': x['default'], 'ux_category': x['ux_category']}, axis=1)
        df = df.drop(['input_type', 'input_format', 'description', 'default', 'ux_category'], axis=1)
        result = {'name': df.Subfilter.values[0], 'kor_name': df.Subfilter_KOR.values[0], 'input': df.input.values[0], 'user_view': df.user_view.values[0]}

    return json.dumps(result, ensure_ascii=False, indent=4)


###### SEARCH FILTER #####
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI
# http://127.0.0.1:5000/?PriceFilter.dist_max=60,in
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.compare_max=0.7
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.updown=1000,10000&PriceFilter.compare_max=0.7
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.updown=1000,10000&PriceFilter.compare_max=0.7&CrossFilter.goldencross=5,20
@app.route('/', methods=['GET', ])
def filter():
    start_time = time.time()

    # mysql connecting info & connect
    conn, curs = connect_db()

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

    # ????????? ???????????? ????????? ?????? ??????
    if len(df) == 0:
        return "????????? ???????????? ????????? ????????????."

    # result??? ????????? ?????? ??????
    cols = ['Name', 'ID', 'Close', 'Volume', 'DaytoDay']
    df = df[cols]

    # one_year_before??? ????????? ?????? ??????
    ids = df.ID.to_list()
    one_year_ago_date_sql = "SELECT Date FROM stocksearch.past_market WHERE Date <= date_add(now(), interval -1 year) GROUP BY Date ORDER BY Date DESC LIMIT 1;"  # 1??? ??? ??????
    curs.execute(one_year_ago_date_sql)
    one_year_ago_date = curs.fetchone()[0]
    one_year_ago_date = one_year_ago_date.strftime("%Y-%m-%d")

    where_str = ''
    for id in ids:
        where_str += f'ID = "{id}" or '
    where_str = where_str[:-3]  # ????????? 'or ' ??????
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

    # ?????? log??? DB??? ??????
    save_request_log(query, curs, conn)

    print("--- %s seconds ---" % (time.time() - start_time))

    return json.dumps(answer, ensure_ascii=False, indent=4)


###### DICTIONARY #####
# http://127.0.0.1:5000/dictionary
# http://127.0.0.1:5000/dictionary/2
@app.route('/dictionary/', methods=['GET', ])
@app.route('/dictionary/<int:Dic_SN>', methods=['GET', ])
def dic(Dic_SN=None):
    # mysql connecting info & connect
    conn, curs = connect_db()

    if Dic_SN == None:
        total_df = pd.read_sql("SELECT Dic_SN, Title FROM stocksearch.dictionary;", conn)
        answer = total_df.to_dict('records')

    else:
        curs.execute(f"SELECT * FROM stocksearch.dictionary WHERE Dic_SN = {Dic_SN};")
        dic_data = curs.fetchone()
        answer = dict(zip(['Dic_SN', 'Title', 'Summary', 'Description', 'Condition'], dic_data))
        print(answer)

    return json.dumps(answer, ensure_ascii=False, indent=4)


###### Board #####
# ????????? searchfilter??? ????????? ??? ?????? ??????????????? ??????
def save_request_log(request, curs, conn):
    sql = f"INSERT INTO stocksearch.request_history (query) VALUES ('{request}')"
    curs.execute(sql)
    conn.commit()


# ??????????????? -> ???????????? ???????????? ????????? ??????
def proc_query(query):
    query_li = query.split('&')
    proc_str = ''
    for q in query_li:
        f = q.split('=')[0]
        proc_str += f+','
    return proc_str


# http://127.0.0.1:5000/board/recent
@app.route('/board/recent/', methods=['GET', ])
def board_recent():
    # mysql connecting info & connect
    conn, curs = connect_db()

    # ?????? 7??? ??? ???????????? ??????
    sql = "SELECT * FROM stocksearch.request_history WHERE date(update_date) >= date(now())-7 ORDER BY update_date DESC;"
    board_df = pd.read_sql(sql, conn)
    # ????????????,????????? ???????????? ??????????????? drop, ?????? 10??? ??????????????? ??????
    board_df['filter_ori'] = board_df.Query.apply(lambda x: proc_query(x))
    board_df = board_df.drop_duplicates(['filter_ori']).head(10)

    return board_df[['Query']].to_json(orient='index')


# http://127.0.0.1:5000/board/famous
@app.route('/board/famous/', methods=['GET', ])
def board_famous():
    # mysql connecting info & connect
    conn, curs = connect_db()

    # ?????? 7??? ??? ???????????? ??????
    sql = "SELECT * FROM stocksearch.request_history WHERE date(update_date) >= date(now())-7 ORDER BY update_date DESC;"
    board_df = pd.read_sql(sql, conn)
    # ??? ?????? ??? ?????? ??????
    history = []
    for f in board_df.Query:
        f_li = f.split('&')
        for f_detail in f_li:
            history.append(f_detail)
    query_count = Counter(history)
    # ?????? ?????? ??????
    queries = sorted(query_count, key=query_count.get, reverse=True)

    return json.dumps(queries[:10])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True)
