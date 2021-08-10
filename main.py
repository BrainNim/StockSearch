import pymysql
import pandas as pd
from flask import Flask, request, jsonify
from search_filter import *

# connect mysql
conn = pymysql.connect(host="localhost",
                       user="root",
                       password="0000",
                       db="stocksearch")

# Flask run
app = Flask(__name__)

# http://127.0.0.1:5000/?MarketFilter.market=KOSPI
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.compare_max=0.7
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.compare_max=0.7&MarketFilter.market=KOSDAQ
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.updown=1000,10000&PriceFilter.compare_max=0.7
@app.route('/')
def filter():
    df = pd.read_sql("select * from stocksearch.daily_market", conn)

    query = request.query_string.decode('utf-8')
    parameters = query.split('&')

    if len(parameters) == 0:
        return df.ID.to_string()

    for param in parameters:
        func = param.split('=')[0].split('.')[0]
        method = param.split('=')[0].split('.')[-1]
        values = param.split('=')[-1]
        filter_func = getattr(globals()[func](conn), method)
        df = filter_func(values, df)

    return str(df.ID.to_list())

if __name__ == "__main__":
    app.run()