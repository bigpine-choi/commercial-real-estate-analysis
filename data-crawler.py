import requests
import pandas as pd

# API 정보
API_KEY = "63716794310649c0b1e8bc0666df7902"
BASE_URL = "https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do"

# 데이터별 STATBL_ID
RENTAL_STATBL_ID = "TT249843134237374"  # 오피스 임대료 데이터
VACANCY_STATBL_ID = "TT244763134428698"  # 오피스 공실률 데이터

# 전국 + 각 지역 분류 코드 (서울 주요 권역 포함)
region_codes = {
    "서울전체": "500002",
    "GBD": "510003",
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

for region_name, cls_id in region_codes.items():
    # 🔹 임대료 데이터 요청
    params_rental = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "STATBL_ID": RENTAL_STATBL_ID,  # 임대료 데이터 코드
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
            print(f"❌ {region_name} 임대료 데이터 없음:", data_rental)
    else:
        print(f"🚨 API 요청 실패 ({region_name} - 임대료):", response_rental.status_code, response_rental.text)

    # 🔹 공실률 데이터 요청
    params_vacancy = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "STATBL_ID": VACANCY_STATBL_ID,  # 공실률 데이터 코드
        "DTACYCLE_CD": "QY",  # 분기별 데이터
        "CLS_ID": cls_id,  # 지역 코드
        "ITM_ID": "100001"  # 공실률 ITM_ID (정확한 값 확인 필요)
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
            print(f"❌ {region_name} 공실률 데이터 없음:", data_vacancy)
    else:
        print(f"🚨 API 요청 실패 ({region_name} - 공실률):", response_vacancy.status_code, response_vacancy.text)

# 🔹 모든 데이터 합치기
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    # CSV로 저장
    final_df.to_csv("오피스_임대료_공실률_서울.csv", encoding="utf-8-sig", index=False)
    print("✅ 모든 지역 임대료 + 공실률 데이터 저장 완료: 오피스_임대료_공실률_서울.csv")
else:
    print("⚠️ 데이터가 없습니다.")