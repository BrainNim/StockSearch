import pandas as pd
import datetime


def mk_temp(df, conn, times=0):
    id_li = df.ID.to_list()
    temp_curs = conn.cursor()
    temp_curs.execute("CREATE TEMPORARY TABLE temp_id(ID VARCHAR(8))")
    temp_curs.executemany("INSERT INTO stocksearch.temp_id (ID) VALUES (%s)", id_li)

    if times > 0:
        for i in range(1, times):
            temp_curs.execute(f"CREATE TEMPORARY TABLE temp{i}_id(ID VARCHAR(8))")
            temp_curs.executemany(f"INSERT INTO stocksearch.temp{i}_id (ID) VALUES (%s)", id_li)


def drop_temp(conn):
    temp_curs = conn.cursor()
    temp_curs.execute("""DROP TEMPORARY TABLE temp_id""")


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
        mk_temp(df, self.conn)
        mean_df = pd.read_sql(f"""SELECT ID, AVG(Close) as Mean FROM
                            (SELECT past.* FROM stocksearch.past_market AS past
                            JOIN temp_id AS id ON past.ID = id.ID) tb
                            WHERE Date >= Date(subdate("{self.recent_date}", INTERVAL {day} DAY))
                            GROUP BY ID;""", self.conn)
        drop_temp(self.conn)
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

        mk_temp(df, self.conn)
        mean_df = pd.read_sql(f"""SELECT ID, AVG(Volume) as Mean FROM
                            (SELECT past.* FROM stocksearch.past_market AS past
                            JOIN temp_id AS id ON past.ID = id.ID) tb
                            WHERE Date >= Date(subdate("{self.recent_date}", INTERVAL {day} DAY))
                            GROUP BY ID;""", self.conn)
        drop_temp(self.conn)
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
        self.schedule = pd.read_sql(f"""SELECT Date FROM stocksearch.past_market GROUP BY Date ORDER BY Date DESC;""", self.conn)
        self.recent_date = self.schedule.iloc[0].values[0]  # 최근 시장오픈

    def get_cross_sql(self, short, long):
        short, long = int(short), int(long)
        short_ago = self.schedule.iloc[short].values[0]
        long_ago = self.schedule.iloc[long].values[0]
        # TS: TodayShort, TL: TodayLong, YS: YesterdayShort, YL:YesterdayLong
        cross_sql = f"""select TS.ID, TS, TL, YS, YL from 
                            (SELECT ID, AVG(Close) as TS FROM (SELECT past.* FROM stocksearch.past_market AS past
                                                                JOIN temp_id AS id ON past.ID = id.ID) tb
                                                        WHERE Date > "{short_ago}"
                                                        GROUP BY ID) as TS
                            join
                            (SELECT ID, AVG(Close) as TL FROM (SELECT past.* FROM stocksearch.past_market AS past
                                                                JOIN temp1_id AS id ON past.ID = id.ID) tb
                                                        WHERE Date > "{long_ago}"
                                                        GROUP BY ID) as TL on TS.ID = TL.ID
                            join
                            (SELECT ID, AVG(Close) as YS FROM (SELECT past.* FROM stocksearch.past_market AS past
                                                                JOIN temp2_id AS id ON past.ID = id.ID) tb
                                                        WHERE Date >= "{short_ago}" and Date < "{self.recent_date}"
                                                        GROUP BY ID) as YS on TS.ID = YS.ID
                            join
                            (SELECT ID, AVG(Close) as YL FROM (SELECT past.* FROM stocksearch.past_market AS past
                                                                JOIN temp3_id AS id ON past.ID = id.ID) tb
                                                        WHERE Date >= "{long_ago}" and Date < Date "{self.recent_date}"
                                                        GROUP BY ID) as YL on TS.ID = YL.ID ;"""
        return cross_sql

    def goldencross(self, short, long, df):
        goldencross_sql = self.get_cross_sql(short, long)
        mk_temp(df, self.conn, times=4)
        mean_df = pd.read_sql(goldencross_sql, self.conn)
        drop_temp(self.conn)

        mean_df = mean_df[(mean_df['TS'] > mean_df['TL']) & (mean_df['YS'] < mean_df['YL'])]
        new_df = pd.merge(mean_df, df, left_on='ID', right_on='ID', how='inner')
        new_df = new_df.drop(['TS', 'TL', 'YS', 'YL'], axis=1)
        return new_df

    def deadcross(self, short, long, df):
        mk_temp(df, self.conn, times=4)
        deadcross_sql = self.get_cross_sql(short, long)
        mean_df = pd.read_sql(deadcross_sql, self.conn)
        mean_df = mean_df[(mean_df['TS'] < mean_df['TL']) & (mean_df['YS'] > mean_df['YL'])]
        new_df = pd.merge(mean_df, df, left_on='ID', right_on='ID', how='inner')
        new_df = new_df.drop(['TS', 'TL', 'YS', 'YL'], axis=1)
        return new_df

# (SELECT past.* FROM stocksearch.past_market AS past
#                                                                 JOIN temp_id AS id ON past.ID = id.ID) tb