import requests
import pandas as pd

# API 정보
API_KEY = "63716794310649c0b1e8bc0666df7902"
BASE_URL = "https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do"

# 데이터별 STATBL_ID (2002~2024년 데이터 포함)
RENTAL_PRICE_STATBL_IDS = {
    "rental price": "TT244963134453269" # 임대동향 지역별 임대가격지수(시계열)_2013-2024
}

VACANCY_STATBL_IDS = {
    "2002-2012": "A_2024_00678",  # 2002년~2012년 데이터
    "2013-2016": "A_2024_00238"  # 2013년~2016년 데이터
}

# 2021년 이후 전국 + 각 지역 분류 코드 (서울 주요 권역 포함)
region_codes_new = {
    "서울전체": "500002",
    "CBD": "510003",
    "GBD": "510004",
    "YBD": "510005",
    "Others": "510006",
    "CBD_광화문": "520004",
    "CBD_남대문": "520005",
    "CBD_동대문": "520006",
    "CBD_명동": "520007",
    "CBD_시청": "520008",
    "CBD_을지로": "520009",
    "CBD_종로": "520010",
    "CBD_충무로": "520011",
    "GBD_강남대로": "520013",
    "GBD_교대역": "520014",
    "GBD_남부터미널": "520015",
    "GBD_논현역": "520016",
    "GBD_도산대로": "520017",
    "GBD_신사역": "520018",
    "GBD_테헤란로": "520019",
    "YBD_공덕역": "520021",
    "YBD_당산역": "520022",
    "YBD_여의도": "520023",
    "YBD_영등포역": "520024",
    "Others_목동": "520026",
    "Others_사당": "520027",
    "Others_숙명여대": "520028",
    "Others_용산역": "520029",
    "Others_잠실송파": "520030",
    "Others_잠실새내": "520031",
    "Others_장안동": "520032",
    "Others_천호": "520033",
    "Others_홍대합정": "520034",
    "Others_화곡": "520035"
}

# 결과 저장할 리스트
all_data = []

for period, rental_statbl_id in RENTAL_STATBL_IDS.items():
    vacancy_statbl_id = VACANCY_STATBL_IDS[period]  # 같은 기간의 공실률 ID 사용

    # 📌 **2021년 이후 지역 분류코드 사용**
    if period in ["2021", "2022-2024Q2", "2024Q3 이후"]:
        region_codes = region_codes_new
    elif period == "2020":
        region_codes = region_codes_2020
    elif period == "2019":
        region_codes = region_codes_2019
    elif period == "2017-2018":
        region_codes = region_codes_20172018
    elif period == "2013-2016":
        region_codes = region_codes_20132016
    else:
        region_codes = region_codes_20022012

    for region_name, cls_id in region_codes.items():
        # 🔹 임대료 데이터 요청
        params_rental = {
            "KEY": API_KEY,
            "Type": "json",
            "pIndex": 1,
            "pSize": 100,
            "STATBL_ID": rental_statbl_id,  # 임대료 데이터 코드
            "DTACYCLE_CD": "QY",  # 분기별 데이터
            "CLS_ID": cls_id,  # 지역 코드
            "ITM_ID": "100001"  # 임대료 ITM_ID
        }

        response_rental = requests.get(BASE_URL, params=params_rental)

        if response_rental.status_code == 200:
            data_rental = response_rental.json()
            if "SttsApiTblData" in data_rental:
                rental_data = data_rental["SttsApiTblData"][1]["row"]
                df_rental = pd.DataFrame(rental_data)
                df_rental["지역"] = region_name
                df_rental["지표"] = "임대료"
                all_data.append(df_rental)
            else:
                print(f"❌ {region_name} 임대료 데이터 없음 ({period}):", data_rental)
        else:
            print(f"🚨 API 요청 실패 ({region_name} - 임대료 {period}):", response_rental.status_code, response_rental.text)

        # 🔹 공실률 데이터 요청
        params_vacancy = {
            "KEY": API_KEY,
            "Type": "json",
            "pIndex": 1,
            "pSize": 100,
            "STATBL_ID": vacancy_statbl_id,  # 공실률 데이터 코드
            "DTACYCLE_CD": "QY",  # 분기별 데이터
            "CLS_ID": cls_id,  # 지역 코드
            "ITM_ID": "100001"  # 공실률 ITM_ID
        }

        response_vacancy = requests.get(BASE_URL, params=params_vacancy)

        if response_vacancy.status_code == 200:
            data_vacancy = response_vacancy.json()
            if "SttsApiTblData" in data_vacancy:
                vacancy_data = data_vacancy["SttsApiTblData"][1]["row"]
                df_vacancy = pd.DataFrame(vacancy_data)
                df_vacancy["지역"] = region_name
                df_vacancy["지표"] = "공실률"
                all_data.append(df_vacancy)
            else:
                print(f"❌ {region_name} 공실률 데이터 없음 ({period}):", data_vacancy)
        else:
            print(f"🚨 API 요청 실패 ({region_name} - 공실률 {period}):", response_vacancy.status_code, response_vacancy.text)

# 🔹 모든 데이터 합치기
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    # 🔹 시간순 정렬 + CLS_ID 오름차순 정렬
    final_df = final_df.sort_values(by=["WRTTIME_DESC","CLS_ID"], ascending=[True,True])

    # CSV로 저장
    final_df.to_csv("오피스_임대료_공실률_서울_시간순.csv", encoding="utf-8-sig", index=False)
    print("✅ 모든 지역 임대료 + 공실률 데이터 저장 완료: 오피스_임대료_공실률_서울_시간순.csv")
else:
    print("⚠️ 데이터가 없습니다.")