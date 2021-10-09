import requests
from bs4 import BeautifulSoup

def from_same_upjong_per(conn):

    curs = conn.cursor()

    url = f"https://finance.naver.com/sise/sise_group.naver?type=upjong"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    upjong_soup = soup.select_one("table.type_1")
    upjongs = upjong_soup.select("tr > td > a")

    for i in range(len(upjongs)):
        cat_id = int(upjongs[i]['href'].split('=')[-1])
        category = upjongs[i].get_text()
        curs.execute(f"""INSERT INTO stocksearch.category (ID, Category) VALUES ({cat_id}, '{category}')
                    ON DUPLICATE KEY UPDATE ID={cat_id}, Category='{category}'; """)

    conn.commit()