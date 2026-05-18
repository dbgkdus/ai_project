# Streamlit + Folium 서울 관광지 TOP10 앱

## app.py

```python
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지 TOP10", layout="wide")

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("지도에서 관광지를 클릭하면 가까운 지하철역과 놀거리를 확인할 수 있습니다.")

# 관광지 데이터
places = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "subway": "경복궁역",
        "fun": "한복 체험, 북촌한옥마을 산책"
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "subway": "명동역",
        "fun": "쇼핑, 길거리 음식 투어"
    },
    {
        "name": "남산서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "subway": "명동역",
        "fun": "야경 감상, 케이블카 체험"
    },
    {
        "name": "홍대거리",
        "lat": 37.5563,
        "lon": 126.9220,
        "subway": "홍대입구역",
        "fun": "버스킹 공연, 카페 탐방"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "subway": "안국역",
        "fun": "전통 한옥 구경, 사진 촬영"
    },
    {
        "name": "롯데월드타워",
        "lat": 37.513068,
        "lon": 127.102926,
        "subway": "잠실역",
        "fun": "전망대 관람, 쇼핑몰 방문"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.566526,
        "lon": 127.009223,
        "subway": "동대문역사문화공원역",
        "fun": "야간 산책, 패션 쇼핑"
    },
    {
        "name": "코엑스",
        "lat": 37.512535,
        "lon": 127.058220,
        "subway": "삼성역",
        "fun": "별마당도서관, 아쿠아리움 관람"
    },
    {
        "name": "광장시장",
        "lat": 37.570388,
        "lon": 126.999096,
        "subway": "종로5가역",
        "fun": "빈대떡 먹방, 전통시장 체험"
    },
    {
        "name": "한강공원",
        "lat": 37.528316,
        "lon": 126.932455,
        "subway": "여의나루역",
        "fun": "자전거 타기, 치맥 피크닉"
    }
]

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# 세션 상태 초기화
if "selected_place" not in st.session_state:
    st.session_state.selected_place = None

# 마커 추가
for place in places:
    popup_html = f"""
    <b>{place['name']}</b><br>
    클릭해서 상세 정보 확인
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=popup_html,
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# 지도 출력
map_data = st_folium(m, width=1200, height=600)

# 클릭 이벤트 처리
if map_data and map_data.get("last_object_clicked_popup"):
    clicked_name = map_data["last_object_clicked_popup"].split("<br>")[0].replace("<b>", "").replace("</b>", "")

    for place in places:
        if place["name"] == clicked_name:
            st.session_state.selected_place = place

# 하단 정보 출력
st.markdown("---")
st.subheader("📍 관광지 정보")

if st.session_state.selected_place:
    selected = st.session_state.selected_place

    st.success(
        f"{selected['name']} → 가까운 지하철역: {selected['subway']} | 놀거리: {selected['fun']}"
    )
else:
    st.info("지도에서 관광지를 클릭해보세요!")
```

---

## requirements.txt

```txt
streamlit
folium
streamlit-folium
```

---

## 실행 방법

### 1. 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 2. 앱 실행

```bash
streamlit run app.py
```

---

## Streamlit Cloud 배포 방법

1. GitHub 저장소 생성
2. `app.py` 와 `requirements.txt` 업로드
3. urlStreamlit Cloud[https://share.streamlit.io](https://share.streamlit.io) 접속
4. GitHub 저장소 연결 후 배포
