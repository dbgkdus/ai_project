import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울 도시고속도로 분석",
    layout="wide"
)

st.title("🚗 서울 도시고속도로 혼잡도 분석")

uploaded_file = st.file_uploader(
    "CSV 파일 업로드",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

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

    traffic_row = df[
        (df["구분"] == "2025년 평균") &
        (df["교통량"] == "교통량")
    ].iloc[0]

    speed_row = df[
        (df["구분"] == "2025년 평균") &
        (df["교통량"] == "속도")
    ].iloc[0]

    result = pd.DataFrame({
        "노선": roads,
        "교통량": [traffic_row[r] for r in roads],
        "속도": [speed_row[r] for r in roads]
    })

    result["교통량"] = pd.to_numeric(result["교통량"])
    result["속도"] = pd.to_numeric(result["속도"])

    # 혼잡도 지수
    result["혼잡도"] = result["교통량"] / result["속도"]

    st.subheader("데이터")

    st.dataframe(result, use_container_width=True)

    st.subheader("교통량 순위")

    fig1 = px.bar(
        result.sort_values("교통량", ascending=False),
        x="노선",
        y="교통량",
        color="교통량"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("평균속도 순위")

    fig2 = px.bar(
        result.sort_values("속도"),
        x="노선",
        y="속도",
        color="속도"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("혼잡도 순위")

    fig3 = px.bar(
        result.sort_values("혼잡도", ascending=False),
        x="노선",
        y="혼잡도",
        color="혼잡도"
    )

    st.plotly_chart(fig3, use_container_width=True)

    most_congested = result.sort_values(
        "혼잡도",
        ascending=False
    ).iloc[0]

    st.success(
        f"가장 혼잡한 노선은 "
        f"{most_congested['노선']} 입니다."
    )
