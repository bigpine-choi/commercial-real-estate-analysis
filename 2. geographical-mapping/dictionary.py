# ✅ CLS_NM을 도로명 주소로 매핑
cls_nm_to_address = {
    "서울": "서울특별시 종로구 세종대로 172",
    "여의도마포": "서울특별시 영등포구 국제금융로 10",
    "강남": "서울특별시 강남구 테헤란로 152",
    "기타": "서울특별시 은평구 수색로 215"
}

# ✅ CLS_NM을 도로명 주소로 변환
df_latest["주소"] = df_latest["CLS_NM"].map(cls_nm_to_address)

# ✅ 변환된 주소 확인
print(df_latest[["CLS_NM", "주소"]].drop_duplicates())
