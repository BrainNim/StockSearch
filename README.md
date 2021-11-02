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
         "kor_name":"마켓필터",
         "subfilter":[
            {
               "filter_SN":1,
               "name":"market",
               "kor_name":"코스피/코스닥"
            },
            {
               "filter_SN":2,
               "name":"category",
               "kor_name":"업종"
            }
         ]
      },
      {
         "name":"PriceFilter",
         "kor_name":"현재가필터",
         "subfilter":[
            {
               "filter_SN":3,
               "name":"updown",
               "kor_name":"이상/이하 범위"
            },
            {
               "filter_SN":4,
               "name":"compare_mean",
               "kor_name":"기간평균대비"
            },
            {
               "filter_SN":5,
               "name":"compare_max",
               "kor_name":"최고가대비"
            },
            {
               "filter_SN":6,
               "name":"dist_max",
               "kor_name":"최고가일과의 날짜"
            }
         ]
      }
   ]
}
	
```
</div>
</details>

### 서브필터 세부항목 조회
예시) ```http://127.0.0.1:5000/filter_li/1```

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
   "limit":"필터입력값제한범위",
   "ux_category":"카테고리번호"
}
```

<details>
<summary>출력예시 (접기/펼치기)</summary>
<div markdown="1">

```json
{
   "name":"updown",
   "kor_name":"이상/이하 범위",
   "input":{
      "type":"min,max",
      "data_format":"int,int"
   },
   "user_view":{
      "description":"('min' < 현재가 < 'max')에 부합하는 종목",
      "limit":"0,9999999",
      "ux_category":2
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

### BongFilter
| 세부필터     |입력값수| 입력값상세                 | 설명                                             | 쿼리예시                      |
|--------------|-------|----------------------------|--------------------------------------------------|-------------------------------|
| shape        | 1     | shape  </br>(str)          | 오늘의 캔들모양이 ('shape')에 부합하는 종목       | BongFilter.shape=Bullish      |

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
```
{
   "Dic_SN": 사전목록번호<Number>,
   "Title": "제목"<String>,
   "Summary": "간단요약"<String>,
   "Description":"설명+사진"<String>,
   "Condition":"조건검색쿼리"<String>
}
```


<details>
<summary>출력예시 (접기/펼치기)</summary>
<div markdown="1">

```json
{
   "Dic_SN":4,
   "Title":"PER(주가수익비율), 이 주식은 저평가일까?",
   "Summary":"- 주식가치가 고평가 됐는지 가늠할 수 있는 기초적인 잣대\\\\n- 주가/주당순이익\\\\n- 낮을수록 저평가, 높을수록 고평가",
   "Description":"흔히들 저평가 된 주식을 찾으라고들 하죠.\\n하지만, 그래서 뭐가 저평가 된 주식인데?\\nPER(주가수익비율)은 주식의 가치를 가늠할 수 있는 기초적인 잣대예요.\\n\\n주가가 많이 오르거나, 배당을 많이 받으려면 그 회사에 순이익이 높아야 해요. 그리고 한 주당 가격이 낮은 주식을 산다면, 우리는 같은 금액으로 더 많은 이윤을 챙길 수 있겠죠? 아무리 회사의 순이익이 높다 한들, 이미 주가가 높다면 많은 이윤을 얻기는 힘들거예요.\\n\\n그래서 PER은 (주가/주당순이익)으로 주식의 가치를 계산해본 지표예요.\\n높을수록 고평가, 낮을수록 저평가 되었다고 볼 수 있어요.\\nA회사는 현재주가가 2만원이고 1주당 순이익이 4000원이라서 PER=2만/4천=5 예요.\\nB회사는 현재주가가 1만원이고 1주당 순이익이 500원이라서 PER=1만/5백=20 이예요.\\nA회사의 PER가 더 낮으니 B회사보다는 상대적으로 저평가 되었군요!\\n가격이 싼 주식만 찾았다면 B회사의 주식을 살 뻔했죠?\\n\\n하지만 PER가 낮은 주식만 찾는 건 곤란해요.\\n예를들어, 업종별로 PER 평균도 따져보는게 좋아요. C전자회사의 PER가 40이고, D식품회사의 PER가 20이라면 C전자회사가 훨씬 고평가 되어있는 것 같지만, 만약 전기전자업종의 평균PER가 60이고, 식품업종의 평균PER가 15라면, 오히려 C전자회사가 저평가 되었다고 해석할 수도 있거든요.\\n\\n그리고 낮은 PER의 주식이 아닌, 높은 PER의 주식을 선별해 투자하는 고PER 전략의 투자도 있으니 여러가지를 꼼꼼하게 살펴보는게 좋아요.\\n\\n그럼 이번에 배운 PER를 활용해서 내 입맛에 맞는 종목을 찾아보러 가볼까요?",
   "Condition":"PERFilter.bottom=20"
}
```
</div>
</details>


## 게시판조회
요청예시)  
``` localhost:5000/board/ ```  

#### 검색 횟수 상위의 필터조합 조회
``` /board/ ```
