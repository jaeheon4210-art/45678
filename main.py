import pandas as pd
import plotly.express as px
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("1년간 박스오피스 10위권에 진입했던 개봉작 216편의 장르, 국가, 스크린수, 관객수 등의 분포와 상관관계를 분석함.")

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 열 전처리: 세로막대(|)로 구분된 복수 장르 중 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()
    
    # 수치형 데이터 캐스팅
    numeric_columns = ["first_scrn", "first_show", "first_week_audi", "total_audi", "days_in_top10"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        
    return df

# 데이터 로딩
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ 데이터를 불러오는 중 오류가 발생함: {e}")
    st.stop()

st.divider()

# ==========================================
# 📌 구역 1: 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.header("🍩 섹션 1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화편수"]

# Plotly 도넛 그래프 생성 (hole=0.4 설정으로 중앙이 비어있는 형태)
fig1 = px.pie(
    genre_counts,
    values="영화편수",
    names="장르",
    title="🍕 개봉 영화 장르별 편수 비중",
    hole=0.4
)

# 마우스 호버 시 편수와 비율이 모두 표시되도록 설정
fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르:</b> %{label}<br><b>영화 편수:</b> %{value}편<br><b>점유율:</b> %{percent}<extra></extra>"
)

fig1.update_layout(
    legend_title_text="장르 선택 (클릭 시 토글)"
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** "
    "1년 동안 박스오피스 상위권에 진입한 영화들의 장르 다변화 정도와 특정 대표 장르의 시장 편중 현상을 한눈에 파악할 수 있음."
)
