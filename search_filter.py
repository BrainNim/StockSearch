import pandas as pd
import datetime


class MarketFilter:
    def market(market, df):
        new_df = df[df['Market'] == market]
        return new_df

    def category(category, df):
        new_df = df[df['Market'] == category]
        return new_df


class PriceFilter:
    def updown(down, up, df):
        new_df = df[(df['Close'] <= up) & (df['Close'] >= down)]
        return new_df

    def compare_mean(day, times, updown, df, conn):  # 기간평균가와 현재가 비교
        code_tuple = tuple(df['ID'])
        mean_df = pd.read_sql(f"""SELECT ID, AVG(Close) as Mean  FROM stocksearch.past_market 
                            WHERE Date >= Date(subdate(now(), INTERVAL {day} DAY))
                            GROUP BY ID;""", conn)
        new_df = pd.merge(mean_df, df, left_on='ID', right_on='ID', how='inner')
        if updown == 'up':
            new_df = new_df[new_df['Close'] >= new_df['Mean'] * times]
        else:
            new_df = new_df[new_df['Close'] <= new_df['Mean'] * times]
        new_df = new_df.drop('Mean', axis=1)
        return new_df

    def compare_max(times, df):  # 250일 최고가와 현재가 비교
        new_df = df[df['Close'] <= df['Highest_Price'] * times]
        return new_df

    def dist_max(day, inout, df):  # 250일 최고가와 현재가 비교
        cont_day = datetime.datetime.now() - datetime.timedelta(days=day)
        if inout == 'in':
            new_df = df[df['Highest_Date'] >= cont_day.date()]
        else:
            new_df = df[df['Highest_Date'] <= cont_day.date()]
        return new_df


class VolumeFilter:
    def updown(down, up, df):
        new_df = df[(df['Volume'] <= up) & (df['Volume'] >= down)]
        return new_df

    def compare_mean(day, times, updown, df, conn):
        mean_df = pd.read_sql(f"""SELECT ID, AVG(Volume) as Mean FROM stocksearch.past_market 
                            WHERE Date >= Date(subdate(now(), INTERVAL {day} DAY))
                            GROUP BY ID;""", conn)
        new_df = pd.merge(mean_df, df, left_on='ID', right_on='ID', how='inner')
        if updown == 'up':
            new_df = new_df[new_df['Volume'] >= new_df['Mean'] * times]
        else:
            new_df = new_df[new_df['Volume'] <= new_df['Mean'] * times]
        new_df = new_df.drop('Mean', axis=1)
        return new_df

    def compare_max(times, df, conn):
        for code in df['ID']:
            new_df = pd.read_sql(f"""SELECT ID, MAX(Volume) as Max FROM stocksearch.past_market 
                        WHERE ID = '{code}' """, conn)


class PBRFilter:
    def updown(down, up, df):
        new_df = df[(df['PBR'] <= up) & (df['PBR'] >= down)]
        return new_df

    def top(topdown, n, df):
        if topdown == 'top':
            new_df = df.sort_values(by='PBR', ascending=False).head(n)
        else:
            new_df = df.sort_values(by='PBR', ascending=True).head(n)
        return new_df


class PERFilter:
    def updown(down, up, df):
        new_df = df[(df['PER'] <= up) & (df['PER'] >= down)]
        return new_df

    def top(topdown, n, df):
        if topdown == 'top':
            new_df = df.sort_values(by='PER', ascending=False).head(n)
        else:
            new_df = df.sort_values(by='PER', ascending=True).head(n)
        return new_df


class ROAFilter:
    def updown(down, up, df):
        new_df = df[(df['ROA'] <= up) & (df['ROA'] >= down)]
        return new_df

    def top(topdown, n, df):
        if topdown == 'top':
            new_df = df.sort_values(by='ROA', ascending=False).head(n)
        else:
            new_df = df.sort_values(by='ROA', ascending=True).head(n)
        return new_df


class ROEFilter:
    def updown(down, up, df):
        new_df = df[(df['ROE'] <= up) & (df['ROE'] >= down)]
        return new_df

    def top(topdown, n, df):
        if topdown == 'top':
            new_df = df.sort_values(by='ROE', ascending=False).head(n)
        else:
            new_df = df.sort_values(by='ROE', ascending=True).head(n)
        return new_df