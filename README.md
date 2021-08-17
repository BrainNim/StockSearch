# StockSearch (가제: 나도주주, 주린이를 위한 기술분석서치 가이드)
기술분석과 투자를 위한 주식종목검색 어플리케이션 개발


## 함수 및 쿼리
| 필터         | 세부필터     |입력값수| 입력값상세       | 설명                                                   | 쿼리예시                              |
|--------------|--------------|-------|------------------|-------------------------------------------------------|---------------------------------------|
| MarketFilter | market       | 1     | market           | market(시장: KOSPI/KOSDAQ)구분                        | MarketFilter.market=KOSPI             |
|              | category     | 1     | category         | category(업종: 식품,자동차,화학 등)구분                | MarketFilter.category=car             |
| PriceFilter  | updown       | 2     | min,max          | ('min' < 현재가 < 'max')에 부합하는 종목               | PriceFilter.updown=1000,10000         |
|              | compare_mean | 3     | day,times,updown | (현재가가 'day'기간 평균가의 'times'배 'updwon(이상/이하)')에 부합하는 종목 | PriceFilter.compare_mean=365,0.5,down |
|              | compare_max  | 1     | times            | (현재가가 1년-250영업일-중 최고가의 'times'배 이하)에 부합하는 종목 | PriceFilter.compare_max=0.7 |
|              | dist_max     | 2     | day,inout        | 1년-250영업일-중 최고가일과 오늘과의 차이가 'day'일 'inout(이내/초과)')에 부합하는 종목 | PriceFilter.dist_max=90,out |
