import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="청소년 복지 통합 허브", layout="wide")
st.title("📊 청소년 복지시설 및 상담센터 이용률 증진을 위한 통합 홍보 플랫폼")
st.caption("빅데이터경영공학 전공 & 청소년복지론 융합 프로젝트 (여성가족부 2024 실태조사 데이터 반영)")

# 2. 사용자가 찾아온 실제 통계 데이터 구조화 (전체, 성별, 연령별)
raw_data = {
    "전체 소계": {"모름": 68.3, "앎": 31.7, "미이용": 70.4, "이용": 29.6},
    "남자": {"모름": 67.5, "앎": 32.5, "미이용": 64.8, "이용": 35.2},
    "여자": {"모름": 69.0, "앎": 31.0, "미이용": 75.9, "이용": 24.1},
    "9~11세 초등학생": {"모름": 76.2, "앎": 23.8, "미이용": 28.1, "이용": 71.9},
    "12~15세 중학생": {"모름": 72.4, "앎": 27.6, "미이용": 73.8, "이용": 26.2},
    "16~18세 고등학생": {"모름": 64.8, "앎": 35.2, "미이용": 71.1, "이용": 28.9}
}

# 3. 사이드바 인터랙티브 필터 구성
st.sidebar.header("🔍 통계 데이터 필터링")
st.sidebar.write("분석하고 싶은 청소년 대상 그룹을 선택하세요.")
selected_group = st.sidebar.selectbox(
    "대상 그룹 선택:",
    list(raw_data.keys())
)

# 선택된 그룹의 데이터 가져오기
group_stats = raw_data[selected_group]

# 그래프용 데이터프레임 변환
df_knowledge = pd.DataFrame({
    "구분": ["기관/서비스 모른다", "기관/서비스 안다"],
    "비율(%)": [group_stats["모름"], group_stats["앎"]]
})

df_usage = pd.DataFrame({
    "구분": ["이용해본 적 없다", "이용해본 적 있다"],
    "비율(%)": [group_stats["미이용"], group_stats["이용"]]
})

# 4. 메인 화면 레이아웃 좌우 분할
col1, col2 = st.columns([5, 5])

with col1:
    st.subheader(f"📉 [{selected_group}] 복지시설 인지 및 이용 실태")
    st.write(f"여성가족부의 2024년 실제 통계 데이터에 따르면, **{selected_group}** 그룹의 복지 서비스 인지 수준과 실제 이용 경험은 아래와 같이 심각한 불균형을 보이고 있습니다.")
    
    # 인지도 차트
    fig_know = px.bar(df_knowledge, x="구분", y="비율(%)", text="비율(%)", title="1. 복지시설/서비스 인지 여부",
                      color="구분", color_discrete_sequence=["#FF6B6B", "#4D96FF"])
    fig_know.update_traces(texttemplate='%{text}%', textposition='inside')
    st.plotly_chart(fig_know, use_container_width=True)
    
    # 이용률 차트
    fig_use = px.bar(df_usage, x="구분", y="비율(%)", text="비율(%)", title="2. 시설/서비스 실제 이용 여부",
                     color="구분", color_discrete_sequence=["#FFD93D", "#6BCB77"])
    fig_use.update_traces(texttemplate='%{text}%', textposition='inside')
    st.plotly_chart(fig_use, use_container_width=True)

with col2:
    st.subheader("🔗 위기 유형별 맞춤형 시설 매칭 및 홍보 원클릭 연결")
    st.write("청소년들이 '몰라서 이용하지 못하는' 사각지대를 해소하기 위해 위기 유형별로 즉각적인 법적 근거 중심의 전문 기관 매칭 서비스를 제공합니다.")
    
    # 사용자의 선택에 따라 동적으로 화면이 바뀌는 인터랙티브 기능
    crisis = st.selectbox(
        "현재 지원이나 상담이 필요한 위기 영역을 선택하세요:",
        ["선택하세요", "가출 및 비행 위기 (청소년 쉼터)", "학교폭력 및 사이버불링 (도란도란)", "청소년 인권 침해 및 권리구제"]
    )
    
    if crisis == "가출 및 비행 위기 (청소년 쉼터)":
        st.error("🏠 **청소년 쉼터 & 청소년전화 1388**")
        st.markdown("""
        * **주요 기능:** 24시간 긴급 일시 보호, 의식주 제공, 가출 청소년 심리 상담 및 가정 복귀 지원.
        * **근거 법률:** 청소년복지 지원법 제16조 (위기청소년 특별지원 및 쉼터 운영)
        * **상담 전화:** 📞 국번없이 1388
        """)
        st.link_button("👉 청소년전화 1388 공식 사이트 이동", "https://www.cyber1388.kr")
        
    elif crisis == "학교폭력 및 사이버불링 (도란도란)":
        st.warning("🏫 **도란도란 (학교폭력 예방 누리집)**")
        st.markdown("""
        * **주요 기능:** 학교 내외 폭력 피해학생 보호 및 치유 지원, 가해학생 선도, 맞춤형 모바일 상담.
        * **근거 법률:** 학교폭력 예방 및 대책에 관한 법률 (5주차 교안 반영)
        * **신고/상담 전화:** 📞 국번없이 117
        """)
        st.link_button("👉 도란도란 공식 사이트 이동", "https://www.dorandoran.go.kr")
        
    elif crisis == "청소년 인권 침해 및 권리구제":
        st.info("⚖️ **청소년 인권 및 권리구제 기관**")
        st.markdown("""
        * **주요 기능:** 청소년의 기본적·보편적 권리 침해에 대한 상담, 조사 및 권리구제 실천 (3주차 인권 특성 반영).
        * **관련 기관:** 한국청소년상담복지개발원 및 각 지역 학생인권교육센터.
        """)
        st.link_button("👉 한국청소년상담복지개발원 이동", "https://www.kyci.or.kr")

    st.divider()
    st.markdown("### 💡 빅데이터 분석 전공자 관점의 홍보 전략 제안")
    st.info("""
    **"전체 청소년의 68.3%가 복지 제도가 있다는 사실 자체를 모릅니다."** 특히 연령대가 올라갈수록(고등학생 그룹) 기관의 인지도는 소폭 상승하나 이용하지 않는 비율이 공고하게 유지됩니다. 
    이는 기존의 학교 중심 오프라인 홍보 방식의 한계를 증명하며, 청소년기 또래 관계 중심적 특성(2주차 교안)을 결합한 모바일/웹 허브 플랫폼 중심의 디지털 홍보 체계 개편이 시급함을 시사합니다.
    """)

# 5. 하단 지도 시각화 레이아웃
st.divider()
st.subheader("📍 우리 지역 청소년 복지 시설 위치 찾기 (인터랙티브 맵)")
st.write("공공데이터포털의 위치 데이터를 연계한 전국의 주요 청소년 안전 인프라 지도 매핑 예시 화면입니다.")

# 가상의 경위도 데이터 생성
map_data = pd.DataFrame({
    "lat": [37.5665, 37.5326, 37.4200, 37.5000],
    "lon": [126.9780, 127.0246, 127.1000, 126.9000],
    "name": ["서울 청소년 단기 쉼터", "도란도란 종합상담소", "위기청소년 중앙지원센터", "1388 긴급구조대"]
})

st.map(map_data)
