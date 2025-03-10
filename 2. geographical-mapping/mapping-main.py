from geopy.geocoders import Nominatim
import time
import pandas as pd

# ✅ 지오코더 객체 생성
geolocator = Nominatim(user_agent="geo_batch_geocoder")

# ✅ 조회할 도로명 주소 리스트
addresses = [
    "서울특별시 중구 세종대로 110",  # 서울전체(서울시청)
    "서울특별시 종로구 세종대로 172",  # 도심지역(광화문)
    "서울특별시 영등포구 국제금융로 10",  # 여의도마포지역(IFC)
    "서울특별시 강남구 테헤란로 152",  # 강남지역(강남역 5번 출구)
    "서울특별시 은평구 수색로 215"  # 기타지역(수색/증산 뉴타운)
]

# ✅ 결과 저장용 리스트
geo_data = []

# ✅ 주소별 위도/경도 변환
for address in addresses:
    try:
        location = geolocator.geocode(address)
        if location:
            lat, lon = location.latitude, location.longitude
            print(f"📍 {address} → 위도 {lat}, 경도 {lon}")
            geo_data.append([address, lat, lon])
        else:
            print(f"❌ {address} → 위치를 찾을 수 없습니다.")
            geo_data.append([address, None, None])
    except Exception as e:
        print(f"⚠️ 오류 발생: {address} → {e}")
        geo_data.append([address, None, None])

    time.sleep(0.1)  # API 호출 제한 방지를 위해 0.1초 대기

# ✅ 변환된 데이터를 DataFrame으로 저장
geo_df = pd.DataFrame(geo_data, columns=["주소", "위도", "경도"])

# ✅ CSV 파일로 저장 (필요 시)
geo_df.to_csv("도로명주소_위도경도_main.csv", encoding="utf-8-sig", index=False)

print("✅ 모든 주소의 위도/경도 변환 완료! CSV 저장 완료.")