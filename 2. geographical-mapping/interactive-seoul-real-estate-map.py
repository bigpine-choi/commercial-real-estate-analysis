import folium
import pandas as pd

# ✅ 데이터 로드
file_path = "오피스_임대료_공실률_투자수익률_순영업소득_main.csv"
geo_file_path = "도로명주소_위도경도_main.csv"

df = pd.read_csv(file_path, encoding="utf-8-sig")
geo_df = pd.read_csv(geo_file_path, encoding="utf-8-sig")

# ✅ 가장 최신 분기 데이터 선택
latest_quarter = df["WRTTIME_DESC"].max()

# ✅ CLS_NM을 도로명 주소로 매핑
cls_nm_to_address = {
    "서울": "서울특별시 중구 세종대로 110",
    "도심": "서울특별시 종로구 세종대로 172",
    "여의도마포": "서울특별시 영등포구 국제금융로 10",
    "강남": "서울특별시 강남구 테헤란로 152",
    "기타": "서울특별시 은평구 수색로 215"
}

# ✅ 가장 최신 분기 데이터 선택 (명확한 복사본 생성)
df_latest = df[df["WRTTIME_DESC"] == latest_quarter].copy()

# ✅ CLS_NM을 도로명 주소로 변환
df_latest["주소"] = df_latest["CLS_NM"].map(cls_nm_to_address).fillna("서울특별시 은평구 수색로 215")

# ✅ 변환된 주소 확인
print("📌 변환된 주소 매핑 결과:")
print(df_latest[["CLS_NM", "주소"]].drop_duplicates())

# ✅ 위도/경도 데이터 병합
df_latest = df_latest.merge(geo_df, left_on="주소", right_on="주소", how="left")

# ✅ 서울 중심 좌표 설정 (광화문 기준)
seoul_center = [37.5665, 126.9780]

# ✅ folium 지도 객체 생성
m = folium.Map(location=seoul_center, zoom_start=12)

# ✅ 지도에 데이터 추가
for idx, row in df_latest.iterrows():
    if pd.notna(row["위도"]) and pd.notna(row["경도"]):  # 유효한 위도/경도만 처리
        # ✅ 각 지표별 값 가져오기
        rental_price = df_latest[(df_latest["CLS_NM"] == row["CLS_NM"]) & (df_latest["지표"] == "임대료")]["DTA_VAL"].values
        vacancy_rate = df_latest[(df_latest["CLS_NM"] == row["CLS_NM"]) & (df_latest["지표"] == "공실률")]["DTA_VAL"].values
        investment_return = df_latest[(df_latest["CLS_NM"] == row["CLS_NM"]) & (df_latest["지표"] == "투자수익률")][
            "DTA_VAL"].values
        noi = df_latest[(df_latest["CLS_NM"] == row["CLS_NM"]) & (df_latest["지표"] == "순영업소득")]["DTA_VAL"].values

        # ✅ 값이 존재하면 가져오고, 없으면 'N/A' 처리 후 소수점 둘째 자리까지 반올림
        rental_price = round(rental_price[0], 2) if len(rental_price) > 0 else "N/A"
        vacancy_rate = round(vacancy_rate[0], 2) if len(vacancy_rate) > 0 else "N/A"
        investment_return = round(investment_return[0], 2) if len(investment_return) > 0 else "N/A"
        noi = round(noi[0], 2) if len(noi) > 0 else "N/A"

        # ✅ folium Marker 추가
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=f"""
                <b>지역:</b> {row['CLS_NM']}<br>
                <b>임대료:</b> {rental_price}천원/제곱m<br>
                <b>공실률:</b> {vacancy_rate}%<br>
                <b>투자수익률:</b> {investment_return}%<br>
                <b>순영업소득:</b> {noi}천원/제곱m
            """,
            tooltip=row["CLS_NM"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# ✅ HTML 파일로 저장
m.save("seoul_real_estate_map.html")
print("✅ 인터랙티브 지도 저장 완료: seoul_real_estate_map.html")
