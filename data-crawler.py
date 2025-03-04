import requests
import pandas as pd

# API 정보
API_KEY = "63716794310649c0b1e8bc0666df7902"
BASE_URL = "https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do"

# 전국 + 각 지역 분류 코드 (전국, 서울, 부산, 대구, 인천, 광주, 대전, 울산, 경기, 강원)
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
    # 요청 파라미터 설정
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "STATBL_ID": "TT249843134237374",  # 오피스 임대료 데이터
        "DTACYCLE_CD": "QY",  # 분기별 데이터
        "CLS_ID": cls_id,  # 지역 코드 (반복문으로 변경)
        "ITM_ID": "100001"  # 임대료
    }

    # API 요청
    response = requests.get(BASE_URL, params=params)

    # 응답 데이터 확인
    if response.status_code == 200:
        data = response.json()
        if "SttsApiTblData" in data:
            rental_data = data["SttsApiTblData"][1]["row"]  # 필요한 데이터 추출
            df = pd.DataFrame(rental_data)  # DataFrame 변환
            df["지역"] = region_name  # 지역명 컬럼 추가
            all_data.append(df)
        else:
            print(f"❌ {region_name} 데이터 없음:", data)
    else:
        print(f"🚨 API 요청 실패 ({region_name}):", response.status_code, response.text)

# 모든 지역 데이터 합치기
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    # CSV로 저장
    final_df.to_csv("오피스_임대료_서울.csv", encoding="utf-8-sig", index=False)
    print("✅ 모든 지역 데이터 저장 완료: 오피스_임대료_서울.csv")
else:
    print("⚠️ 데이터가 없습니다.")