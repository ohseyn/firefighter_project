import pandas as pd
import numpy as np

## 데이터 불러오기
df = pd.read_csv("data/fire.csv")
df

df.columns


## 데이터 전처리
data_2020 = df[['항목'] + df.filter(like='2020').columns.tolist()]
data_2020

data_2021 = df[['항목'] + df.filter(like='2021').columns.tolist()]
data_2021

data_2022 = df[['항목'] + df.filter(like='2022').columns.tolist()]
data_2022

# 제품결함 열(2022.11) 없애줌
data_2022 = data_2022.drop(columns = "2022.11")
data_2022.columns

# 0번째 행을 열로 가져오기
data_2020.columns = data_2020.iloc[0] #0번째 행을 열로
data_2020

data_2021.columns = data_2021.iloc[0] #0번째 행을 열로
data_2021

data_2022.columns = data_2022.iloc[0] #0번째 행을 열로
data_2022


data_2020 = data_2020[2:]
data_2020
data_2020 = data_2020.reset_index(drop=True)
data_2020

data_2021 = data_2021[2:]
data_2021
data_2021 = data_2021.reset_index(drop=True)
data_2021

data_2022 = data_2022[2:]
data_2022
data_2022 = data_2022.reset_index(drop=True)
data_2022

data_2022.info() # 데이터타입 확인

# 문자형을 숫자형으로 변환
# 변환할 열 목록
columns_to_convert = ['계', '전기적요인', '기계적요인',
                '화학적요인', '가스누출', '교통사고', '부주의', '기타',
                '자연적요인', '방화', '방화의심', '미상']

# 각 열에 대해 pd.to_numeric 적용
for column in columns_to_convert:
    data_2020[column] = pd.to_numeric(data_2020[column])

data_2020.info()

for column in columns_to_convert:
    data_2021[column] = pd.to_numeric(data_2021[column])

data_2021.info()

for column in columns_to_convert:
    data_2022[column] = pd.to_numeric(data_2022[column])

data_2022.info()


# 파생변수 만들기
data_2020["계절"] = np.where(data_2020["항목"].isin(["3월", "4월", "5월"]),"spring",
                    np.where(data_2020["항목"].isin(["6월", "7월", "8월"]),"summer",
                    np.where(data_2020["항목"].isin(["9월", "10월", "11월"]),"fall",
                    "winter")))
data_2020

data_2021["계절"] = np.where(data_2021["항목"].isin(["3월", "4월", "5월"]),"spring",
                    np.where(data_2021["항목"].isin(["6월", "7월", "8월"]),"summer",
                    np.where(data_2021["항목"].isin(["9월", "10월", "11월"]),"fall",
                    "winter")))

data_2021

data_2022["계절"] = np.where(data_2022["항목"].isin(["3월", "4월", "5월"]),"spring",
                    np.where(data_2022["항목"].isin(["6월", "7월", "8월"]),"summer",
                    np.where(data_2022["항목"].isin(["9월", "10월", "11월"]),"fall",
                    "winter")))

data_2022

season_20 = data_2020.groupby('계절').agg(계절별화재=('계','sum'))
season_20
season_20.info() # 데이터프레임 형식임!

season_21 = data_2021.groupby('계절').agg(계절별화재=('계','sum'))
season_21

season_22 = data_2022.groupby('계절').agg(계절별화재=('계','sum'))
season_22


# 그래프
# 20년도 그래프를 그림- > 21년도그림 -> 22년도그림 (같이 나오게:지피티한테 물어보기)
# 변수명 바꾸기
season_20 = season_20.rename(columns={"계절별화재" : "2020"})
season_21 = season_21.rename(columns={"계절별화재" : "2021"})
season_22 = season_22.rename(columns={"계절별화재" : "2022"})

# 열로 합치기
season = pd.concat([season_20,season_21,season_22], axis=1)
season

# 계절 순서를 '봄', '여름', '가을', '겨울'로 재정렬
season = season.loc[['spring', 'summer', 'fall', 'winter']]


## 그래프 시각화
## 연도별, 계절별 그래프
import matplotlib.pyplot as plt
#plt.clf()

plt.figure(figsize=(6, 6))
plt.plot(season.index, season['2020'], marker='o', label='2020')
plt.plot(season.index, season['2021'], marker='o', label='2021')
plt.plot(season.index, season['2022'], marker='o', label='2022')

plt.legend()
plt.grid(True)
plt.show()


## 요인 막대그래프(3년치 통계)
# 필요없는 열 삭제 & 데이터 합치기
data_2020
data_2021
data_2022

data_all = pd.concat([data_2020, data_2021,data_2022])
data_all
data_all = data_all.drop(columns=['year'])
data_all = data_all.drop(columns=['계'])
data_all


# 요인별 평균 내기
data_all = data_all.transpose()
data_all.columns
data_all = data_all.drop("항목", axis=0)
data_all = data_all.drop("계절", axis=0)
data_all

data_all=data_all.astype(int)
data_all.info()

data_all["total"] = data_all.sum(axis=1)/3
data_all

## 행 밑에 새로운 행(total)추가하는 방법
#data_all.loc["total"] = data_all.sum()
#data_all

## 한글
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 예시: 윈도우 시스템에 있는 맑은 고딕 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 그래프그리기
data_all["total"].plot.bar(rot=0)
plt.xticks(fontsize=7,rotation=45)
plt.show()


plt.clf()
----------------------------------------------------------------------

#요인에 따른 인명피해 
import pandas as pd
#데이터 불러오기
damage = pd.read_csv("data/human_damage.csv")
damage


# 연도별 분류
damage_20 = damage[['항목'] + damage.filter(like='2020').columns.tolist()]
damage_20
damage_21 = damage[['항목'] + damage.filter(like='2021').columns.tolist()]
damage_21
damage_22= damage[['항목'] + damage.filter(like='2022').columns.tolist()]
damage_22

# 0번째 행을 열로 > 합계까지 인덱싱 > 인덱스 재설정 ( 기존 삭제 )
damage_20.columns = damage_20.iloc[0] 
damage_20 = damage_20[1:3]
damage_20 = damage_20.reset_index(drop = True)

damage_21.columns = damage_21.iloc[0] 
damage_21 = damage_21[1:3]
damage_21 = damage_21.reset_index(drop = True)

damage_22.columns = damage_22.iloc[0] 
damage_22 = damage_22[1:3]
damage_22 = damage_22.reset_index(drop = True)

# 필요없는 열 삭제 
damage_20 = damage_20.drop(columns = ["항목", "계"])
damage_21 = damage_21.drop(columns = ["항목", "계"])
damage_22 = damage_22.drop(columns = ["항목", "계","제품결함"])

# 행열 바꾸기
demage_20 = damage_20.transpose()
demage_21 = damage_21.transpose()
demage_22 = damage_22.transpose()

# 데이터 합치기 
demage_21[1]
demage_total = pd.concat([demage_20, demage_21[1], demage_22[1]], axis=1)
demage_total.columns
demage_total.info()

# 사망/부상 분리 (문자열 삭제)
death = demage_total.iloc[::2,1:4]
wound = demage_total.iloc[1::2,1:4]
death.info()
wound.info()

# 숫자형으로 바꾸기
death = death.apply(pd.to_numeric, errors = 'coerce').astype(np.int64)
death.info()

wound= wound.apply(pd.to_numeric, errors = 'coerce').astype(np.int64)
wound.info()

## chat gpt
  ##for col in death.columns:death[col] = pd.to_numeric(death[col],error = 'coerce'
  ##death["total"] = death.select_dtypes(include = "number").sum(axis = 1)

# 합계 변수 / 평균 변수 / 백분율 추가하기
death_all = death.assign(total = death.sum(axis = 1),
                         mean = lambda x : x["total"] / 3 ,
                         ratio = (death["mean"] / data_all["total"]) * 100)
             
death_all 

wound_all = wound.assign(total = wound.sum(axis = 1),
                         mean = lambda x : x["total"] / 3,
                         ratio = (wound_all["mean"] / data_all["total"]) * 100)
             
wound_all


# 그래프 만들기

# 건수별 사망률 
death_all["ratio"].plot.bar(rot=0)
plt.xticks(fontsize=4, rotation=20,)
plt.show()
plt.clf()

# 건수별 부상률
wound_all["ratio"].plot.bar(rot=0)
plt.xticks(fontsize=4, rotation=20,)
plt.show()
plt.clf()





