import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ✅ 파라미터 설정
time_steps = 8  # 과거 8분기 사용
predict_steps = 4  # 향후 4분기 예측
target_column = "투자수익률"
feature_columns = ["임대료", "공실률", "순영업소득", "투자수익률"]

# ✅ 데이터 로딩
df = pd.read_csv("오피스_임대료_공실률_투자수익률_순영업소득_main.csv", encoding="utf-8-sig")

# ✅ 함수: 지역별 예측 파이프라인
def predict_for_region(region_name):
    region_df = df[df["CLS_NM"] == region_name].copy()
    region_df = region_df.sort_values("WRTTIME_DESC")

    # ✅ 피벗: 시계열 데이터 구조화
    pivot_df = region_df.pivot(index="WRTTIME_DESC", columns="지표", values="DTA_VAL")[feature_columns].dropna()

    # ✅ 표준화
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(pivot_df)

    # ✅ 시퀀스 생성
    X, y = [], []
    for i in range(len(scaled_data) - time_steps - predict_steps + 1):
        X.append(scaled_data[i:i+time_steps])
        y.append(scaled_data[i+time_steps:i+time_steps+predict_steps, 3])  # 투자수익률

    X = np.array(X)
    y = np.array(y)

    # ✅ 모델 구성
    model = Sequential()
    model.add(LSTM(64, activation="relu", input_shape=(time_steps, X.shape[2])))
    model.add(Dense(predict_steps))
    model.compile(optimizer="adam", loss="mse")

    # ✅ 학습
    model.fit(X, y, epochs=100, batch_size=8, verbose=0)

    # ✅ 예측 (가장 최근 시점 기준)
    last_sequence = scaled_data[-time_steps:]
    last_sequence = np.expand_dims(last_sequence, axis=0)
    future_pred_scaled = model.predict(last_sequence)
    future_pred = scaler.inverse_transform(
        np.concatenate([np.zeros((predict_steps, 3)), future_pred_scaled.reshape(-1, 1)], axis=1)
    )[:, -1]  # 투자수익률 복원

    return pivot_df.index[-1], future_pred

# ✅ 전체 지역 반복 적용
results = {}
for region in df["CLS_NM"].unique():
    try:
        last_date, forecast = predict_for_region(region)
        results[region] = forecast
        print(f"✅ {region} 완료 | 마지막 분기: {last_date} | 예측값: {np.round(forecast, 2)}")
    except Exception as e:
        print(f"⚠️ {region} 예측 실패: {e}")

# ✅ 결과 정리
result_df = pd.DataFrame(results).T
result_df.columns = [f"예측_{i+1}분기후" for i in range(predict_steps)]
result_df["예측평균"] = result_df.mean(axis=1)
result_df = result_df.sort_values("예측평균", ascending=False)

# ✅ 결과 출력 및 저장
print("\n📌 향후 투자수익률 예측 결과 (상위 지역):")
print(result_df.head())

result_df.to_csv("LSTM_예측_투자수익률_지역별.csv", encoding="utf-8-sig")