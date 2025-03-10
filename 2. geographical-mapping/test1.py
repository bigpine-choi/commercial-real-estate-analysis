import folium

# 서울 지도 생성 (위도 37.5665, 경도 126.9780 → 서울 중심부)
seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 주요 지역 데이터 (예제)
locations = [
    {"지역명": "강남", "위도": 37.4979, "경도": 127.0276, "임대료": 35000, "공실률": 5.2, "투자수익률": 4.8},
    {"지역명": "여의도", "위도": 37.5281, "경도": 126.9249, "임대료": 28000, "공실률": 7.1, "투자수익률": 4.5},
    {"지역명": "광화문", "위도": 37.5716, "경도": 126.9769, "임대료": 30000, "공실률": 6.8, "투자수익률": 4.7},
]

# 각 지역에 마커 추가
for loc in locations:
    popup_text = f"""
    <b>{loc["지역명"]}</b><br>
    📌 임대료: {loc["임대료"]} 원<br>
    📌 공실률: {loc["공실률"]} %<br>
    📌 투자수익률: {loc["투자수익률"]} %<br>
    """
    folium.Marker(
        location=[loc["위도"], loc["경도"]],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=loc["지역명"]
    ).add_to(seoul_map)

# HTML 파일로 저장
seoul_map.save("seoul_interactive_map.html")
print("✅ 인터랙티브 지도 저장 완료! seoul_interactive_map.html 파일을 열어보세요.")