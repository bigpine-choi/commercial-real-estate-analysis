import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# API 정보
API_KEY = "63716794310649c0b1e8bc0666df7902"
BASE_URL = "https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do"

# 데이터별 STATBL_ID 정의 (2002~2024년 데이터 포함)
data_types = {
    "임대료": {
        "2002-2012": "A_2024_00680", "2013-2016": "A_2024_00257",
        "2017-2018": "A_2024_00261", "2019": "A_2024_00265",
        "2020": "A_2024_00269", "2021": "A_2024_00273",
        "2022-2024Q2": "A_2024_00277", "2024Q3 이후": "TT249843134237374"
    },
    "공실률": {
        "2002-2012": "A_2024_00678", "2013-2016": "A_2024_00238",
        "2017-2018": "A_2024_00241", "2019": "A_2024_00244",
        "2020": "A_2024_00247", "2021": "A_2024_00250",
        "2022-2024Q2": "A_2024_00253", "2024Q3 이후": "TT244763134428698"
    },
    "투자수익률": {
        "2002-2012": "A_2024_00682", "2013-2016": "A_2024_00346",
        "2017-2018": "A_2024_00350", "2019": "A_2024_00354",
        "2020": "A_2024_00358", "2021": "A_2024_00362",
        "2022-2024Q2": "A_2024_00366", "2024Q3 이후": "T245883135037859"
    },
    "순영업소득": {
        "2013-2016": "A_2024_00418", "2017-2018": "A_2024_00422",
        "2019": "A_2024_00426", "2020": "A_2024_00430",
        "2021": "A_2024_00434", "2022-2024Q2": "A_2024_00438",
        "2024Q3 이후": "TT242303134253883"
    }
}

# 지역 분류 코드 설정
region_codes = {
    "2021": {
        "서울전체": "500002", "CBD": "510003", "GBD": "510004", "YBD": "510005", "Others": "510006"
    },
    "2020": {
        "서울전체": "500002", "CBD": "510003", "GBD": "510004", "YBD": "510005", "Others": "510006"
    },
    "2019": {
        "서울전체": "500002", "CBD": "510003", "GBD": "510004", "YBD": "510005", "Others": "510006"
    },
    "2017-2018": {
        "서울전체": "500002", "CBD": "510003", "GBD": "510004", "YBD": "510005", "Others": "510006"
    },
    "2013-2016": {
        "서울전체": "500002", "CBD": "510003", "GBD": "510004", "YBD": "510005", "Others": "510006"
    },
    "2002-2012": {
        "서울전체": "500002", "CBD": "510003", "YBD": "510004", "GBD": "510005", "Others": "510006"
    }
}


# 데이터 요청 함수
def fetch_data_for_region(params, data_type):
    response = requests.get(BASE_URL, params=params)
    print(f"🔍 요청 URL: {response.url}")  # 요청 URL 확인

    if response.status_code == 200:
        data = response.json()
        if "RESULT" in data and data["RESULT"]["CODE"] == "INFO-200":
            return None
        elif "SttsApiTblData" in data:
            df = pd.DataFrame(data["SttsApiTblData"][1]["row"])
            df["지표"] = data_type  # 데이터 유형 추가
            return df
    return None


# 데이터 크롤링 실행 함수
def fetch_office_data(save_csv=True):
    all_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for data_type, statbl_dict in data_types.items():
            for period, statbl_id in statbl_dict.items():
                region_set = region_codes.get(period, region_codes["2002-2012"])  # 지역 코드 매칭

                for region_name, cls_id in region_set.items():
                    params = {
                        "KEY": API_KEY,
                        "Type": "json",
                        "pIndex": 1,
                        "pSize": 100,
                        "STATBL_ID": statbl_id,
                        "DTACYCLE_CD": "QY",
                        "CLS_ID": cls_id,
                        "ITM_ID": "100001"
                    }
                    futures.append(executor.submit(fetch_data_for_region, params, data_type))

        for f in futures:
            result = f.result()
            if result is not None:
                all_data.append(result)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values(by=["WRTTIME_DESC", "CLS_ID", "지표"], ascending=[True, True, True])

        if save_csv:
            final_df.to_csv("오피스_임대료_공실률_투자수익률_순영업소득_main.csv", encoding="utf-8-sig", index=False)
            print("✅ 데이터 저장 완료: 오피스_임대료_공실률_투자수익률_순영업소득_main.csv")

        print(final_df.head())  # 데이터 확인용
        return final_df

    print("⚠️ 데이터가 없습니다.")
    return None


# 실행
fetch_office_data()