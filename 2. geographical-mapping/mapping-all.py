from geopy.geocoders import Nominatim
import time
import pandas as pd

# ✅ 지오코더 객체 생성
geolocator = Nominatim(user_agent="geo_batch_geocoder")

# ✅ 조회할 도로명 주소 리스트
addresses = [
    "서울특별시 중구 새문안로 92",  # CBD-신문로지역(서울신문사)
    "서울특별시 종로구 우정국로 26",  # CBD-우정국로지역(옛 중앙우체국)
    "서울특별시 중구 무교로 21",  # CBD-무교지역(SFC)
    "서울특별시 중구 청계천로 100",  # CBD-청계지역(청계광장)
    "서울특별시 중구 한강대로 405",  # CBD-서울역지역(서울역)
    "서울특별시 중구 남대문시장4길 21",  # CBD-남대문지역(남대문시장 중앙상가)
    "서울특별시 중구 명동길 74",  # CBD-명동지역(명동 중앙상가)
    "서울특별시 중구 을지로 3가 100",  # CBD-기타지역(을지로3가역)
    "서울특별시 마포구 마포대로 109",  # YBD-마포지역(마포역)
    "서울특별시 영등포구 의사당대로 1",  # YBD-국회앞지역(국회의사당)
    "서울특별시 영등포구 국제금융로 10",  # YBD-여의도중앙지역(IFC)
    "서울특별시 영등포구 여의대로 66",  # YBD-증권거래소지역(한국거래소)
    "서울특별시 영등포구 경인로 846",  # YBD-영등포지역(영등포역)
    "서울특별시 강남구",  # GBD-방배지역
    "서울특별시 강남구",  # GBD-서초지역
    "서울특별시 강남구",  # GBD-도산로지역
    "서울특별시 강남구",  # GBD-역삼북부지역
    "서울특별시 강남구",  # GBD-선릉북부지역
    "서울특별시 강남구",  # GBD-삼성북부지역
    "서울특별시 강남구",  # GBD-역삼남부지역
    "서울특별시 강남구",  # GBD-선릉남부지역
    "서울특별시 강남구",  # GBD-삼성남부지역
    "서울특별시 강남구",  # GBD-양재지역
    "서울특별시 강남구",  # GBD-송파지역
    "서울특별시 강남구",  # Others-충정로지역
    "서울특별시 강남구",  # Others-노원지역
    "서울특별시 강남구",  # Others-동대문성동지역
    "서울특별시 강남구",  # Others-용산지역
    "서울특별시 강남구",  # Others-강서목동지역
    "서울특별시 강남구",  # Others-구로지역
    "서울특별시 강남구",  # Others-사당지역
    "서울특별시 강남구",  # Others-천호지역
    "서울특별시 종로구",  # 도심
    "서울특별시 종로구",  # 강남
    "서울특별시 종로구",  # 여의도마포
    "서울특별시 종로구",  # 기타
    "서울특별시 종로구",  # CBD-광화문
    "서울특별시 종로구",  # CBD-동대문
    "서울특별시 종로구",  # CBD-명동
    "서울특별시 종로구",  # CBD-종로
    "서울특별시 종로구",  # CBD-충무로
    "서울특별시 종로구",  # GBD-강남대로
    "서울특별시 종로구",  # GBD-도산대로
    "서울특별시 종로구",  # GBD-서초
    "서울특별시 종로구",  # GBD-테헤란로
    "서울특별시 종로구",  # YBD-공덕역
    "서울특별시 종로구",  # YBD-여의도
    "서울특별시 종로구",  # YBD-영등포
    "서울특별시 종로구",  # Others-목동
    "서울특별시 종로구",  # Others-사당
    "서울특별시 종로구",  # Others-용산
    "서울특별시 종로구",  # Others-잠실
    "서울특별시 종로구",  # Others-장안동
    "서울특별시 종로구",  # Others-천호
    "서울특별시 종로구",  # Others-화곡
    "서울특별시 종로구",  # GBD-논현역
    "서울특별시 종로구",  # GBD-신사역
    "서울특별시 종로구",  # CBD-남대문
    "서울특별시 종로구",  # CBD-시청
    "서울특별시 종로구",  # CBD-을지로
    "서울특별시 종로구",  # GBD-교대역
    "서울특별시 종로구",  # GBD-남부터미널
    "서울특별시 종로구",  # YBD-당산역
    "서울특별시 종로구",  # YBD-영등포역
    "서울특별시 종로구",  # Others-숙명여대
    "서울특별시 종로구",  # Others-용산역
    "서울특별시 종로구",  # Others-잠실/송파
    "서울특별시 종로구",  # Others-잠실새내역
    "서울특별시 종로구"  # Others-홍대/합정
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
geo_df.to_csv("도로명주소_위도경도.csv", encoding="utf-8-sig", index=False)

print("✅ 모든 주소의 위도/경도 변환 완료! CSV 저장 완료.")