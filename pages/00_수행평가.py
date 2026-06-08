# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# -----------------------------
# 한글 폰트 설정
# -----------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding='cp949')

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df['날짜'] = pd.to_datetime(df['날짜'])

    # 월/일/연도 추출
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    df['연도'] = df['날짜'].dt.year

    return df

df = load_data()

# -----------------------------
# 제목
# -----------------------------
st.title("서울 특정 날짜 기온 변화 분석")

st.markdown("""
원하는 월과 일을 선택하면  
해당 날짜의 연도별 최고/최저 기온 변화를 확인할 수 있습니다.
""")

# -----------------------------
# 월 / 일 선택
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox("월 선택", list(range(1, 13)))

with col2:
    day = st.selectbox("일 선택", list(range(1, 32)))

# -----------------------------
# 데이터 필터링
# -----------------------------
filtered = df[
    (df['월'] == month) &
    (df['일'] == day)
].copy()

# 결측치 제거
filtered = filtered.dropna(subset=['최고기온(℃)', '최저기온(℃)'])

# -----------------------------
# 그래프
# -----------------------------
if len(filtered) > 0:

    fig, ax = plt.subplots(figsize=(14, 6))

    # 배경색
    fig.patch.set_facecolor('#f2f2f2')
    ax.set_facecolor('#f2f2f2')

    # 최고기온
    ax.plot(
        filtered['연도'],
        filtered['최고기온(℃)'],
        color='hotpink',
        linewidth=2.5,
        label='최고기온'
    )

    # 최저기온
    ax.plot(
        filtered['연도'],
        filtered['최저기온(℃)'],
        color='#87CEFA',
        linewidth=2.5,
        label='최저기온'
    )

    # 제목
    ax.set_title(
        f"{month}월 {day}일 연도별 기온 변화",
        fontsize=18,
        fontweight='bold'
    )

    # 축 이름
    ax.set_xlabel("연도", fontsize=13)
    ax.set_ylabel("기온(℃)", fontsize=13)

    # 격자
    ax.grid(alpha=0.3)

    # 범례
    ax.legend(fontsize=12)

    st.pyplot(fig)

    # 데이터 보기
    with st.expander("데이터 보기"):
        st.dataframe(
            filtered[['연도', '최고기온(℃)', '최저기온(℃)']]
            .reset_index(drop=True)
        )

else:
    st.warning("선택한 날짜의 데이터가 없습니다.")
