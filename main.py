import pymysql
import pandas as pd
from flask import Flask, request
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
# http://127.0.0.1:5000/?MarketFilter.market=KOSPI&PriceFilter.updown=1000,10000&PriceFilter.compare_max=0.7
@app.route('/')
def filter():

    df = pd.read_sql("select * from stocksearch.daily_market", conn)

    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return df.ID.to_string()

    # http://127.0.0.1:5000/?MarketFilter=market:KOSPI&PriceFilter=updown:1000,10000&PriceFilter=compare_max:0.7
    # for key in parameter_dict.keys():
    #     func = key
    #     method = request.args[key].split(':')[0]
    #     values = request.args[key].split(':')[-1].split(',')

    s = ""
    for key in parameter_dict.keys():
        func = key.split('.')[0]
        method = key.split('.')[-1]

        values = request.args[key].split(',')
        s += f"{func} / {method} / {values} \n"

        filter = getattr(globals()[func](conn), method)
        print()
        print(values[0], type(values[0]))
        print()
        df = filter(values[0], df)

    # return s
    return str(df.ID.to_list())

if __name__ == "__main__":
    app.run()