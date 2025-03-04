import requests
import pandas as pd

# API 정보
API_KEY = "63716794310649c0b1e8bc0666df7902"
BASE_URL = "https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do"

# 요청 파라미터 설정
params = {
    "KEY": API_KEY,
    "Type": "json",
    "pIndex": 1,
    "pSize": 100,
    "STATBL_ID": "TT249843134237374",  # 오피스 임대료 데이터
    "DTACYCLE_CD": "QY",  # 월별 데이터 요청
    "CLS_ID": "500002",
    "ITM_ID": "100001"
}

# API 요청 보내기
response = requests.get(BASE_URL, params=params)

# 응답 데이터 확인 및 DataFrame 변환
if response.status_code == 200:
    data = response.json()
    if "SttsApiTblData" in data:
        rental_data = data["SttsApiTblData"][1]["row"]  # 필요한 데이터 추출
        df = pd.DataFrame(rental_data)  # DataFrame 변환
        print(df.head())  # 데이터 미리보기
    else:
        print("데이터 없음:", data)
else:
    print("API 요청 실패:", response.status_code, response.text)

# DataFrame을 CSV 파일로 저장
df.to_csv("office_rental_data.csv", index=False, encoding="utf-8-sig")

print("CSV 파일 저장 완료: office_rental_data.csv")