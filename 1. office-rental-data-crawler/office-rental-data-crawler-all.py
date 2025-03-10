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
    },
    "2020": {
        "CBD_광화문": "520004",
        "CBD_남대문": "520005",
        "CBD_동대문": "520006",
        "CBD_명동": "520007",
        "CBD_시청": "520008",
        "CBD_을지로": "520009",
        "CBD_종로": "520010",
        "CBD_충무로": "520011",
        "GBD_강남대로": "520013",
        "GBD_논현역": "520014",
        "GBD_도산대로": "520015",
        "GBD_서초": "520016",
        "GBD_신사역": "520017",
        "GBD_테헤란로": "520018",
        "YBD_공덕역": "520020",
        "YBD_여의도": "520021",
        "YBD_영등포": "520022",
        "Others_목동": "520024",
        "Others_사당": "520025",
        "Others_용산": "520026",
        "Others_잠실": "520027",
        "Others_장안동": "520028",
        "Others_천호": "520029",
        "Others_화곡": "520031"
    },
    "2019": {
        "CBD_광화문": "520004",
        "CBD_동대문": "520005",
        "CBD_명동": "520006",
        "CBD_남대문": "520007",
        "CBD_시청": "520008",
        "CBD_을지로": "520009",
        "CBD_종로": "520010",
        "CBD_충무로": "520011",
        "GBD_강남대로": "520013",
        "GBD_논현역": "520014",
        "GBD_도산대로": "520015",
        "GBD_서초": "520016",
        "GBD_신사역": "520017",
        "GBD_테헤란로": "520018",
        "YBD_공덕역": "520020",
        "YBD_여의도": "520021",
        "YBD_영등포": "520022",
        "Others_목동": "520024",
        "Others_사당": "520025",
        "Others_용산": "520026",
        "Others_잠실": "520027",
        "Others_장안동": "520028",
        "Others_천호": "520029",
        "Others_화곡": "520031"
    },
    "2017-2018": {
        "CBD_광화문": "520004",
        "CBD_동대문": "520005",
        "CBD_명동": "520006",
        "CBD_종로": "520008",
        "CBD_충무로": "520009",
        "GBD_강남대로": "520011",
        "GBD_논현역": "520012",
        "GBD_도산대로": "520013",
        "GBD_서초": "520014",
        "GBD_신사역": "520015",
        "GBD_테헤란로": "520016",
        "YBD_공덕역": "520018",
        "YBD_여의도": "520019",
        "YBD_영등포": "520020",
        "Others_목동": "520022",
        "Others_사당": "520023",
        "Others_용산": "520024",
        "Others_잠실": "520025",
        "Others_장안동": "520026",
        "Others_천호": "520027",
        "Others_화곡": "520029"
    },
    "2013-2016": {
        "CBD_광화문": "520004",
        "CBD_동대문": "520005",
        "CBD_명동": "520006",
        "CBD_종로": "520008",
        "CBD_충무로": "520009",
        "GBD_강남대로": "520011",
        "GBD_도산대로": "520012",
        "GBD_서초": "520013",
        "GBD_테헤란로": "520015",
        "YBD_공덕역": "520017",
        "YBD_여의도": "520018",
        "YBD_영등포": "520019",
        "Others_목동": "520021",
        "Others_사당": "520022",
        "Others_용산": "520023",
        "Others_잠실": "520024",
        "Others_장안동": "520025",
        "Others_천호": "520026",
        "Others_화곡": "520028"
    },
    "2002-2012": {
        "CBD_신문로": "520004",
        "CBD_우정국로": "520005",
        "CBD_무교": "520006",
        "CBD_청계": "520007",
        "CBD_서울역": "520008",
        "CBD_남대문": "520009",
        "CBD_명동": "520010",
        "CBD_기타": "520011",
        "YBD_마포": "520013",
        "YBD_국회앞": "520014",
        "YBD_여의도중앙": "520015",
        "YBD_증권거래소": "520016",
        "YBD_영등포": "520017",
        "GBD_방배": "520019",
        "GBD_서초": "520020",
        "GBD_도산대로": "520021",
        "GBD_역삼북부": "520022",
        "GBD_선릉북부": "520023",
        "GBD_삼성북부": "520024",
        "GBD_역삼남부": "520025",
        "GBD_선릉남부": "520026",
        "GBD_삼성남부": "520027",
        "GBD_양재": "520028",
        "GBD_송파": "520029",
        "Others_충정로": "520031",
        "Others_노원": "520032",
        "Others_동대문성동": "520033",
        "Others_용산": "520034",
        "Others_목동": "520035",
        "Others_구로": "520036",
        "Others_사당": "520037",
        "Others_천호": "520038"
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
            final_df.to_csv("오피스_임대료_공실률_투자수익률_순영업소득_all.csv", encoding="utf-8-sig", index=False)
            print("✅ 데이터 저장 완료: 오피스_임대료_공실률_투자수익률_순영업소득_all.csv")

        print(final_df.head())  # 데이터 확인용
        return final_df

    print("⚠️ 데이터가 없습니다.")
    return None


# 실행
fetch_office_data()