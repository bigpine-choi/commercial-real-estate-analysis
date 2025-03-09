# commercial-real-estate-analysis
python 알고리즘을 상업용 부동산 투자에 활용할 방법에 대한 연구 프로젝트(개발중)

1. office-rental-data-crawler-all/main.py:
 한국부동산원 Open API에서 2009~2024년까지 기간의 서울 CBD, GBD, YBD, 기타 4곳의 데이터를 추출하는 main 코드와, 서울을 30여 곳으로 세분화한 all 코드. 2009~2024년 동안 조사된 분기별 상업용 오피스 임대료, 공실률, NOI, 투자수익률 데이터를 수집하여 인공지능에 학습시키기 위한 데이터 추출 과정 처리

2. geographical-mapping-all.py:
 1번의 과정으로부터 추출한 서울 내 30여 곳으로 부터 나온 임대료, 공실률, NOI, 투자수익률 데이터 시각화 및 한국부동산원이 몇 년 주기 마다 조사 지역을 바꿔와서 일부 세부지역의 데이터 연속성이 떨어지는 문제를 보정하기 위한 과정 처리. 카카오 맵 API가 제공하는 실제 지도상의 위도/경도 데이터를 한국부동산원의 데이터에 매핑한 후, 지리적으로 인접한 지역끼리 묶고 평균화하여 데이터 연속성을 보존해주는 과정 처리. 

3. artifitial intelligent learning.py
 TSML 기법으로 인공지능에 다변량 시계열 데이터를 학습시키고 서울 내 30개 지역 중 향후 1~2년 내 투자수익률 상승률 기대값이 가장 높은 투자 유망한 지역을 도출하는 과정 처리.
