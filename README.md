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
| VolumeFilter | updown       | 2     | min,max          | ('min' < 오늘거래량 < 'max')에 부합하는 종목             | VolumeFilter.updown=1000,10000       |
|              | compare_mean | 3     | day,times,updown | (오늘거래량이 'day'기간 평균거래량의 'times'배 'updwon(이상/이하)')에 부합하는 종목 |VolumeFilter.compare_mean=365,0.5,down|
| PBRFilter    | updown       | 2     | min,max          | ('min' < PBR값 < 'max')에 부합하는 종목                   | PBRFilter.updown=1.0,3.0           |
|              | top          | 2     | topdown,N        | (PBR값이 'topdown(상위/하위)' N위)에 부합하는 종목         | PBRFilter.top=top,20               |
| PERFilter    | updown       | 2     | min,max          | ('min' < PER값 < 'max')에 부합하는 종목                   | PERFilter.updown=1.0,3.0           |
|              | top          | 2     | topdown,N        | (PER값이 'topdown(상위/하위)' N위)에 부합하는 종목         | PERFilter.top=top,20               |
| ROAFilter    | updown       | 2     | min,max          | ('min' < ROA값 < 'max')에 부합하는 종목                   | ROAFilter.updown=1.0,3.0           |
|              | top          | 2     | topdown,N        | (ROA값이 'topdown(상위/하위)' N위)에 부합하는 종목         | ROAFilter.top=top,20               |
| ROEFilter    | updown       | 2     | min,max          | ('min' < ROE값 < 'max')에 부합하는 종목                   | ROEFilter.updown=1.0,3.0           |
|              | top          | 2     | topdown,N        | (ROE값이 'topdown(상위/하위)' N위)에 부합하는 종목         | ROEFilter.top=top,20               |
| CrossFilter  | goldencross  | 2     | short,long       | ('short'일선과 'long'일선이 골든크로스)에 부합하는 종목     | CrossFilter.goldencross=5,20       |
|              | deadcross    | 2     | short,long       | ('short'일선과 'long'일선이 데드크로스)에 부합하는 종목     | CrossFilter.daedcross=5,20         |
