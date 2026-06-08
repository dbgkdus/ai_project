import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="서울 도시고속도로 혼잡도 분석",
    layout="wide"
)

st.title("🚗 서울 도시고속도로 혼잡도 분석")

# 프로젝트 전체에서 csv 자동 탐색
csv_files = list(Path.cwd().rglob("*.csv"))

if not csv_files:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.stop()

csv_path = csv_files[0]

df = pd.read_csv(csv_path)

traffic = df[
    (df["구분"] == "2025년 평균")
    & (df["교통량"] == "교통량")
].iloc[0]

speed = df[
    (df["구분"] == "2025년 평균")
    & (df["교통량"] == "속도")
].iloc[0]

roads = [
    "내부순환로",
    "강변북로",
    "북부간선도로",
    "올림픽대로",
    "동부간선도로",
    "분당수서로",
    "경부고속도로",
    "강남순환로"
]

result = pd.DataFrame({
    "노선": roads,
    "교통량": [float(traffic[r]) for r in roads],
    "평균속도": [float(speed[r]) for r in roads]
})

result["혼잡도"] = result["교통량"] / result["평균속도"]

result = result.sort_values(
    "혼잡도",
    ascending=False
)

st.subheader("노선별 혼잡도")

st.dataframe(
    result,
    use_container_width=True
)

fig = px.bar(
    result,
    x="노선",
    y="혼잡도",
    color="혼잡도",
    text_auto=".0f"
)

fig.update_layout(height=600)

st.plotly_chart(
    fig,
    use_container_width=True
)

worst = result.iloc[0]

st.error(
    f"""
가장 혼잡한 노선

🚗 {worst['노선']}

교통량 : {worst['교통량']:,.0f} 대/일

평균속도 : {worst['평균속도']:.1f} km/h

혼잡도 지수 : {worst['혼잡도']:.0f}
"""
)

st.info(
    "현재 파일에는 요일별·시간대별 데이터가 없어 "
    "가장 혼잡한 요일과 시간대는 분석할 수 없습니다."
)
