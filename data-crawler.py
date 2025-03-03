import requests

API_KEY = "eeaac10b8cb1449ca091aa7aa430027e"  # 발급받은 인증키 입력
BASE_URL = "https://api.molit.go.kr/statistics"  # API 엔드포인트 예시 (실제 URL 확인 필요)

# 요청 파라미터 설정 (예: 특정 지역의 임대료 & 공실률 조회)
params = {
    "serviceKey": API_KEY,
    "region": "서울",  # 지역 변경 가능
    "type": "json"
}

# API 요청 보내기
response = requests.get(BASE_URL, params=params)

# 응답 데이터 확인
if response.status_code == 200:
    data = response.json()
    print(data)  # JSON 데이터 출력
else:
    print("API 요청 실패:", response.status_code, response.text)
