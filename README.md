# StockSearch (가제: 나도주주, 주린이를 위한 기술분석서치 가이드)
기술분석과 투자를 위한 주식종목검색 어플리케이션 개발
(pip install lxml, bs4, pandas, )

## 필터조회

### 전체 필터리스트 조회
예시) ```http://127.0.0.1:5000/filter_li```

#### 출력결과(JSON)
```
{
   "filter":[
      {
	 "name":"필터이름(ENG)",
	 "kor_name":"필터이름(KOR)",
         "subfilter":[
            {
               "filter_SN":"메인-세부필터 고유번호"
               "name":"서브필터이름(ENG)",
	       "kor_name":"서브필터이름(KOR)"
            }
         ]
      }
   ]
}
```

<details>
<summary>출력예시 (접기/펼치기)</summary>
<div markdown="1">
  
```json
{
   "filter":[
      {
         "name":"MarketFilter",
         "kor_name":null,
         "subfilter":[
            {
               "filter_SN":1,
               "name":"market",
               "kor_name":null
            },
            {
               "filter_SN":2,
               "name":"category",
               "kor_name":null
            }
         ]
      },
      {
         "name":"PriceFilter",
         "kor_name":null,
         "subfilter":[
            {
               "filter_SN":3,
               "name":"updown",
               "kor_name":null
            },
            {
               "filter_SN":4,
               "name":"compare_mean",
               "kor_name":null
            },
            {
               "filter_SN":5,
               "name":"compare_max",
               "kor_name":null
            },
            {
               "filter_SN":6,
               "name":"dist_max",
               "kor_name":null
            }
         ]
      }
   ]
}
	
```
</div>
</details>

### 서브필터 세부항목 조회
예시) ```http://127.0.0.1:5000/filter_li```

#### 출력결과(JSON)
```json
"name":"필터이름(ENG)",
"kor_name":"필터이름(KOR)",
"input":{
   "type":"입력값구분",
   "data_format":"입력값포맷형식"
},
"user_view":{
   "description":"해당필터설명",
   "default":"필터기본입력값(디폴트값)",
   "ux_category":"카테고리번호"
}
```

<details>
<summary>출력예시 (접기/펼치기)</summary>
<div markdown="1">

```json
{
   "name":"category",
   "kor_name":"업종",
   "input":{
      "type":"category",
      "data_format":"str"
   },
   "user_view":{
      "description":"종목의 업종",
      "default":"자동차",
      "ux_category":1
   }
}
```
</div>
</details>


## 종목검색함수 및 쿼리
예시)  
``` localhost:5000/?MarketFilter.market=KOSPI ```  
``` localhost:5000/?PriceFilter.updown=1000,10000&PriceFilter.compare_max=0.7&CrossFilter.goldencross=5,20 ```

### MarketFilter
| 세부필터      |입력값수| 입력값상세        | 설명                                                       | 쿼리예시                            |
|--------------|-------|-------------------|------------------------------------------------------------|------------------------------------|
| market       | 1     | market </br>(str) | market(시장: KOSPI/KOSDAQ)구분                              | MarketFilter.market=KOSPI          |
| category     | 1     | category</br>(str)| category(업종: 식품,자동차,화학 등)구분                      | MarketFilter.category=car          |

### PriceFilter
| 세부필터      |입력값수| 입력값상세                          | 설명                                                       | 쿼리예시                            |
|--------------|-------|------------------------------------|------------------------------------------------------------|------------------------------------|
| updown       | 2     | min,max              </br>(int,int)| ('min' < 현재가 < 'max')에 부합하는 종목                     | PriceFilter.updown=1000,10000      |
| compare_mean | 3     | day,times,updown </br>(int,flt,str)| (현재가가 'day'기간 평균가의 'times'배 'updwon(이상/이하)')에 부합하는 종목 | PriceFilter.compare_mean=365,0.5,down |
| compare_max  | 1     | times                    </br>(flt)| (현재가가 1년-250영업일-중 최고가의 'times'배 이하)에 부합하는 종목         | PriceFilter.compare_max=0.7 |
| dist_max     | 2     | day,inout            </br>(int,str)| (1년-250영업일-중 최고가일과 오늘과의 차이가 'day'일 'inout(이내/초과)')에 부합하는 종목 | PriceFilter.dist_max=90,out |

### VolumeFilter
| 세부필터      |입력값수| 입력값상세                          | 설명                                                       | 쿼리예시                            |
|--------------|-------|------------------------------------|------------------------------------------------------------|------------------------------------|
| updown       | 2     | min,max              </br>(int,int)| ('min' < 오늘거래량 < 'max')에 부합하는 종목                  | VolumeFilter.updown=1000,10000     |
| compare_mean | 3     | day,times,updown </br>(int,flt,str)| (오늘거래량이 'day'기간 평균거래량의 'times'배 'updwon(이상/이하)')에 부합하는 종목 |VolumeFilter.compare_mean=365,0.5,down|

### PBR, PER, ROA, ROEFilter
| 필터         | 세부필터      |입력값수| 입력값상세                  | 설명                                                       | 쿼리예시                            |
|--------------|--------------|-------|----------------------------|------------------------------------------------------------|------------------------------------|
| PBRFilter    | updown       | 2     | min,max     </br>(flt,flt) | ('min' < PBR값 < 'max')에 부합하는 종목                      | PBRFilter.updown=1.0,3.0           |
|              | top          | 2     | topdown,N   </br>(str,int) | (PBR값이 'topdown(상위/하위)' N위)에 부합하는 종목            | PBRFilter.top=top,20               |
| PERFilter    | updown       | 2     | min,max     </br>(flt,flt) | ('min' < PER값 < 'max')에 부합하는 종목                      | PERFilter.updown=1.0,3.0           |
|              | top          | 2     | topdown,N   </br>(str,int) | (PER값이 'topdown(상위/하위)' N위)에 부합하는 종목            | PERFilter.top=top,20               |
|              | compare_group| 2     | times,updown</br>(flt,str) | (PER값이 동일업종PER의 'times'배 'updown(이상/이하)')에 부합하는 종목| PERFilter.compare_group=0.5,down |
| ROAFilter    | updown       | 2     | min,max     </br>(flt,flt) | ('min' < ROA값 < 'max')에 부합하는 종목                      | ROAFilter.updown=1.0,3.0           |
|              | top          | 2     | topdown,N   </br>(str,int) | (ROA값이 'topdown(상위/하위)' N위)에 부합하는 종목            | ROAFilter.top=top,20               |
| ROEFilter    | updown       | 2     | min,max     </br>(flt,flt) | ('min' < ROE값 < 'max')에 부합하는 종목                      | ROEFilter.updown=1.0,3.0           |
|              | top          | 2     | topdown,N   </br>(str,int) | (ROE값이 'topdown(상위/하위)' N위)에 부합하는 종목            | ROEFilter.top=top,20               |

### CrossFilter
| 세부필터      |입력값수| 입력값상세                 | 설명                                                       | 쿼리예시                            |
|--------------|-------|----------------------------|------------------------------------------------------------|------------------------------------|
| goldencross  | 2     | short,long  </br>(int,int) | ('short'일평균선과 'long'일평균선이 골든크로스)에 부합하는 종목 | CrossFilter.goldencross=5,20       |
| deadcross    | 2     | short,long  </br>(int,int) | ('short'일평균선과 'long'일평균선이 데드크로스)에 부합하는 종목 | CrossFilter.daedcross=5,20         |

### DebtFilter
| 세부필터     |입력값수| 입력값상세                 | 설명                                             | 쿼리예시                  |
|--------------|-------|----------------------------|--------------------------------------------------|---------------------------|
| updown       | 2     | min,max  </br>(flt,flt)    | ('min' < 부채율 < 'max')에 부합하는 종목          | DebtFilter.updown=0,200   |
| continuous   | 1     | quarter  </br>(int)        | 부채율이 'quarter'분기 이상동안 연속 감소한 종목  | DebtFilter.continuous=5   |
  
### RetentionFilter
| 세부필터     |입력값수| 입력값상세                 | 설명                                             | 쿼리예시                      |
|--------------|-------|----------------------------|--------------------------------------------------|-------------------------------|
| updown       | 2     | min,max  </br>(flt,flt)    | ('min' < 유보율 < 'max')에 부합하는 종목          | RetentionFilter.updown=0,20   |
| continuous   | 1     | quarter  </br>(int)        | 유보율이 'quarter'분기 이상동안 연속 증가한 종목  | RetentionFilter.continuous=5  |


### 출력 결과(JSON)
```
{
	"result": [{
		"Name": "종목명"<string>,
		"ID": "종목코드"<string>,
		"Close": 종가(현재가)<number>,
		"Volume": 거래량<number>,
		"DaytoDay": 이전 거래일 대비 가격증감(정수)<number>
	}],
	"one_year_before_date": "1년 전 날자"<string>,
	"one_year_before": [{
		"ID": "종목코드"<string>,
		"Close": 1 년전 종가<number>,
		"rate": 1 년전 대비 수익률(%)<number>
	}]
}
```

<details>
<summary>출력예시 (접기/펼치기)</summary>
<div markdown="1">
  
```json
{
	"result": [{
		"Name": "써니전자",
		"ID": "004770",
		"Close": 3245,
		"Volume": 210758,
		"DaytoDay": 50.0
	}, {
		"Name": "아남전자",
		"ID": "008700",
		"Close": 2615,
		"Volume": 538375,
		"DaytoDay": 0.0
	}, {
		"Name": "에쓰씨엔지니어링",
		"ID": "023960",
		"Close": 4920,
		"Volume": 228605,
		"DaytoDay": -75.0
	}],
	"one_year_before_date": "2020-09-11",
	"one_year_before": [{
		"ID": "004770",
		"Close": 4110,
		"rate": -21.046228710462287
	}, {
		"ID": "008700",
		"Close": 1905,
		"rate": 37.270341207349084
	}, {
		"ID": "023960",
		"Close": 1300,
		"rate": 278.46153846153845
	}]
}
```
</div>
</details>


  
## 주식용어사전
요청예시)  
``` localhost:5000/dictionary/ ```  
``` localhost:5000/dictionary/2 ```

### 사전 전체목록 조회
``` /dictionary/ ```

#### 출력결과(JSON)
```json
[{
	"Dic_SN": 1,
	"Title": "골든크로스"
}, {
	"Dic_SN": 2,
	"Title": "데드크로스"
}]
```

### 특정 항목(용어) 조회
``` /dictionary/<int:Dic_SN> ```

#### 출력결과(JSON)
```json
{
	"Dic_SN": 1,
	"Title": "골든크로스",
	"Description": "블라블라블라",
	"Condition": "CrossFilter.goldencross=5,20"
}
```



## 게시판조회
요청예시)  
``` localhost:5000/board/ ```  

#### 검색 횟수 상위의 필터조합 조회
``` /board/ ```
