import pandas as pd

# 📌 CSV 파일 로드
file_path = "/mnt/data/오피스_임대료_공실률_투자수익률_순영업소득_all.csv"
geo_file_path = "/mnt/data/도로명주소_위도경도.csv"  # 📍 서울 지역 위도/경도 데이터

# ✅ 데이터 로드
df = pd.read_csv(file_path, encoding="utf-8-sig")
geo_df = pd.read_csv(geo_file_path, encoding="utf-8-sig")

# ✅ 데이터 확인
print("📌 데이터 미리보기")
print(df.head())
print("📌 지역 위도/경도 데이터 미리보기")
print(geo_df.head())

# ✅ 가장 최신 분기의 데이터만 선택
latest_quarter = df["WRTTIME_DESC"].max()
df_latest = df[df["WRTTIME_DESC"] == latest_quarter]

# ✅ 위도/경도 데이터와 병합
df_latest = df_latest.merge(geo_df, left_on="CLS_NM", right_on="지역명", how="left")

# ✅ 병합된 데이터 확인
print("📌 최신 분기 데이터 병합 결과:")
print(df_latest.head())
