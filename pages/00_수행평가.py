import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="서울 도시고속도로 혼잡도 분석",
    layout="wide"
)

st.title("🚗 서울 도시고속도로 혼잡도 분석")

# pages 폴더의 상위 폴더
BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "서울시설공단_서울도시고속도로 교통통계 현황_20260428 (1).csv"

df = pd.read_csv(csv_path)

traffic_row = df[
    (df["구분"] == "2025년 평균")
    & (df["교통량"] == "교통량")
].iloc[0]

speed_row = df[
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
    "교통량": [float(traffic_row[r]) for r in roads],
    "속도": [float(speed_row[r]) for r in roads]
})

result["혼잡도"] = result["교통량"] / result["속도"]

result = result.sort_values(
    "혼잡도",
    ascending=False
)

st.subheader("혼잡도 순위")

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

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

worst = result.iloc[0]

st.error(
    f"""
가장 혼잡한 노선

🚨 {worst['노선']}

교통량 : {worst['교통량']:,.0f} 대/일

평균속도 : {worst['속도']:.1f} km/h
"""
)
