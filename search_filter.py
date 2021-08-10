import pandas as pd
import datetime


class MarketFilter:
    def __init__(self, conn):
        self.conn = conn

    def market(self, market, df):
        new_df = df[df['Market'] == market]
        return new_df

    def category(self, category, df):
        new_df = df[df['Market'] == category]
        return new_df


class PriceFilter:
    def __init__(self, conn):
        self.conn = conn
        schedule = pd.read_sql(f"""SELECT Date FROM stocksearch.past_market GROUP BY Date ORDER BY Date DESC;""", conn)
        self.recent_date = schedule.iloc[0].values[0]  # 최근 시장오픈

    def updown(self, down, up, df):
        down, up = float(down), float(up)
        new_df = df[(df['Close'] <= up) & (df['Close'] >= down)]
        return new_df

    def compare_mean(self, day, times, updown, df):  # 기간평균가와 현재가 비교
        day, times = int(day), float(times)
        code_tuple = tuple(df['ID'])
        mean_df = pd.read_sql(f"""SELECT ID, AVG(Close) as Mean  FROM stocksearch.past_market 
                            WHERE Date >= Date(subdate("{self.recent_date}", INTERVAL {day} DAY))
                            GROUP BY ID;""", self.conn)
        new_df = pd.merge(mean_df, df, left_on='ID', right_on='ID', how='inner')
        if updown == 'up':
            new_df = new_df[new_df['Close'] >= new_df['Mean'] * times]
        else:
            new_df = new_df[new_df['Close'] <= new_df['Mean'] * times]
        new_df = new_df.drop('Mean', axis=1)
        return new_df

    def compare_max(self, times, df):  # 250일 최고가와 현재가 비교
        times = float(times)
        new_df = df[df['Close'] <= df['Highest_Price'] * times]
        return new_df

    def dist_max(self, day, inout, df):  # 250일 최고가일이 오늘과 몇일 떨어져있나
        day = int(day)
        cont_day = datetime.datetime.now() - datetime.timedelta(days=day)
        if inout == 'in':
            new_df = df[df['Highest_Date'] >= cont_day.date()]
        else:
            new_df = df[df['Highest_Date'] <= cont_day.date()]
        return new_df


class VolumeFilter:
    def __init__(self, conn):
        self.conn = conn
        schedule = pd.read_sql(f"""SELECT Date FROM stocksearch.past_market GROUP BY Date ORDER BY Date DESC;""", conn)
        self.recent_date = schedule.iloc[0].values[0]  # 최근 시장오픈

    def updown(self, down, up, df):
        down, up = float(down), float(up)
        new_df = df[(df['Volume'] <= up) & (df['Volume'] >= down)]
        return new_df

    def compare_mean(self, day, times, updown, df):
        day, times = int(day), float(times)
        mean_df = pd.read_sql(f"""SELECT ID, AVG(Volume) as Mean FROM stocksearch.past_market 
                            WHERE Date >= Date(subdate("{self.recent_date}", INTERVAL {day} DAY))
                            GROUP BY ID;""", self.conn)
        new_df = pd.merge(mean_df, df, left_on='ID', right_on='ID', how='inner')
        if updown == 'up':
            new_df = new_df[new_df['Volume'] >= new_df['Mean'] * times]
        else:
            new_df = new_df[new_df['Volume'] <= new_df['Mean'] * times]
        new_df = new_df.drop('Mean', axis=1)
        return new_df

    # def compare_max(self, times, df, conn):
    #     for code in df['ID']:
    #         new_df = pd.read_sql(f"""SELECT ID, MAX(Volume) as Max FROM stocksearch.past_market
    #                     WHERE ID = '{code}' """, self.conn)


class PBRFilter:
    def __init__(self, conn):
        self.conn = conn

    def updown(self, down, up, df):
        down, up = float(down), float(up)
        new_df = df[(df['PBR'] <= up) & (df['PBR'] >= down)]
        return new_df

    def top(self, topdown, n, df):
        n = int(n)
        if topdown == 'top':
            new_df = df.sort_values(by='PBR', ascending=False).head(n)
        else:
            new_df = df.sort_values(by='PBR', ascending=True).head(n)
        return new_df


class PERFilter:
    def __init__(self, conn):
        self.conn = conn

    def updown(self, down, up, df):
        down, up = float(down), float(up)
        new_df = df[(df['PER'] <= up) & (df['PER'] >= down)]
        return new_df

    def top(self, topdown, n, df):
        n = int(n)
        if topdown == 'top':
            new_df = df.sort_values(by='PER', ascending=False).head(n)
        else:
            new_df = df.sort_values(by='PER', ascending=True).head(n)
        return new_df


class ROAFilter:
    def __init__(self, conn):
        self.conn = conn

    def updown(self, down, up, df):
        down, up = float(down), float(up)
        new_df = df[(df['ROA'] <= up) & (df['ROA'] >= down)]
        return new_df

    def top(self, topdown, n, df):
        n = int(n)
        if topdown == 'top':
            new_df = df.sort_values(by='ROA', ascending=False).head(n)
        else:
            new_df = df.sort_values(by='ROA', ascending=True).head(n)
        return new_df


class ROEFilter:
    def __init__(self, conn):
        self.conn = conn

    def updown(self, down, up, df):
        down, up = float(down), float(up)
        new_df = df[(df['ROE'] <= up) & (df['ROE'] >= down)]
        return new_df

    def top(self, topdown, n, df):
        n = int(n)
        if topdown == 'top':
            new_df = df.sort_values(by='ROE', ascending=False).head(n)
        else:
            new_df = df.sort_values(by='ROE', ascending=True).head(n)
        return new_df


class CrossFilter:
    def __init__(self, conn):
        self.conn = conn
        schedule = pd.read_sql(f"""SELECT Date FROM stocksearch.past_market GROUP BY Date ORDER BY Date DESC;""", conn)
        self.recent_date = schedule.iloc[0].values[0]  # 최근 시장오픈

    def goldencross(self, short, long, df):
        short, long = int(short), int(long)
        goldencross_sql = f"""select TS.ID, TS, TL, YS, YL from 
                            (SELECT ID, AVG(Close) as TS FROM stocksearch.past_market 
                                                        WHERE Date >= Date(subdate("{self.recent_date}", INTERVAL {short} DAY))
                                                        GROUP BY ID) as TS
                            join
                            (SELECT ID, AVG(Close) as TL FROM stocksearch.past_market 
                                                        WHERE Date >= Date(subdate("{self.recent_date}", INTERVAL {long} DAY))
                                                        GROUP BY ID) as TL on TS.ID = TL.ID
                            join
                            (SELECT ID, AVG(Close) as YS FROM stocksearch.past_market 
                                                        WHERE Date >= Date(subdate"{self.recent_date}", INTERVAL {short}+1 DAY)) and Date < Date(subdate("{self.recent_date}", INTERVAL 1 DAY))
                                                        GROUP BY ID) as YS on TS.ID = YS.ID
                            join
                            (SELECT ID, AVG(Close) as YL FROM stocksearch.past_market 
                                                        WHERE Date >= Date(subdate("{self.recent_date}", INTERVAL {long}+1 DAY)) and Date < Date(subdate("{self.recent_date}", INTERVAL 1 DAY))
                                                        GROUP BY ID) as YL on TS.ID = YL.ID ;"""
        mean_df = pd.read_sql(goldencross_sql, self.conn)
        mean_df = mean_df[(mean_df['TS'] > mean_df['TL']) & (mean_df['YS'] < mean_df['YL'])]
        new_df = pd.merge(mean_df, df, left_on='ID', right_on='ID', how='inner')
        new_df = new_df.drop(['TS', 'TL', 'YS', 'YL'], axis=1)
        return new_df

    def deadcross(self, short, long, df):
        short, long = int(short), int(long)
        deadcross_sql = f"""select TS.ID, TS, TL, YS, YL from 
                            (SELECT ID, AVG(Close) as TS FROM stocksearch.past_market 
                                                        WHERE Date >= Date(subdate(now(), INTERVAL {short} DAY))
                                                        GROUP BY ID) as TS
                            join
                            (SELECT ID, AVG(Close) as TL FROM stocksearch.past_market 
                                                        WHERE Date >= Date(subdate(now(), INTERVAL {long} DAY))
                                                        GROUP BY ID) as TL on TS.ID = TL.ID
                            join
                            (SELECT ID, AVG(Close) as YS FROM stocksearch.past_market 
                                                        WHERE Date >= Date(subdate(now(), INTERVAL {short}+1 DAY)) and Date < Date(subdate(now(), INTERVAL 1 DAY))
                                                        GROUP BY ID) as YS on TS.ID = YS.ID
                            join
                            (SELECT ID, AVG(Close) as YL FROM stocksearch.past_market 
                                                        WHERE Date >= Date(subdate(now(), INTERVAL {long}+1 DAY)) and Date < Date(subdate(now(), INTERVAL 1 DAY))
                                                        GROUP BY ID) as YL on TS.ID = YL.ID ;"""
        mean_df = pd.read_sql(deadcross_sql, self.conn)
        mean_df = mean_df[(mean_df['TS'] < mean_df['TL']) & (mean_df['YS'] > mean_df['YL'])]
        new_df = pd.merge(mean_df, df, left_on='ID', right_on='ID', how='inner')
        new_df = new_df.drop(['TS', 'TL', 'YS', 'YL'], axis=1)
        return new_df

