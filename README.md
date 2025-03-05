# commercial-real-estate-analysis
python 알고리즘을 상업용 부동산 투자에 활용할 방법에 대한 연구 프로젝트(개발중)

1. data-crawler.py:
 한국부동산원 Open API에서 2009~2024년까지 기간의 서울을 30여 곳으로 세분화한 분기별 상업용 오피스 평균 임대료, 공실률, 거래가격 데이터를 수집하여 인공지능에 학습시키기 전까지의 데이터 전처리 과정 처리

2. main.py:
 1번의 과정으로부터 추출한 데이터를 시각화하고 인사이트를 도출하는 과정 처리

3. artifitial intelligent learning.py
 TSML 기법으로 인공지능에 시계열 데이터를 학습시키고 서울 내 30개 지역 중 투자 유망한 지역을 도출하는 과정 처리
