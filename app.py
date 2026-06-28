import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="청소년 복지 통합 허브", layout="wide")
st.title("📊 청소년 복지시설 및 상담센터 이용률 증진을 위한 통합 홍보 플랫폼")
st.caption("빅데이터경영공학 전공 & 청소년복지론 융합 프로젝트 (여성가족부 2024 실태조사 데이터 반영)")

# 2. 사용자가 찾아온 2가지 실제 통계 데이터 연동 (전체, 성별, 연령별)
raw_data = {
    "전체 소계": {
        "모름": 68.3, "앎": 31.7, "미이용": 70.4, "이용": 29.6,
        "경험없음": 72.3, "경험있음": 27.7, "1회": 8.1, "2~3회": 8.1, "4~5회": 4.4, "6~9회": 2.2, "10회이상": 4.9
    },
    "남자": {
        "모름": 67.5, "앎": 32.5, "미이용": 64.8, "이용": 35.2,
        "경험없음": 73.7, "경험있음": 26.3, "1회": 7.2, "2~3회": 9.0, "4~5회": 4.6, "6~9회": 2.4, "10회이상": 3.0
    },
    "여자": {
        "모름": 69.0, "앎": 31.0, "미이용": 75.9, "이용": 24.1,
        "경험없음": 70.9, "경험있음": 29.1, "1회": 8.9, "2~3회": 7.2, "4~5회": 4.2, "6~9회": 2.0, "10회이상": 6.8
    },
    "9~11세 초등학생": {
        "모름": 76.2, "앎": 23.8, "미이용": 28.1, "이용": 71.9,
        "경험없음": 93.1, "경험있음": 6.9, "1회": 2.9, "2~3회": 3.3, "4~5회": 0.4, "6~9회": 0.2, "10회이상": 0.0
    },
    "12~15세 중학생": {
        "모름": 72.4, "앎": 27.6, "미이용": 73.8, "이용": 26.2,
        "경험없음": 72.3, "경험있음": 27.7, "1회": 7.2, "2~3회": 9.7, "4~5회": 3.9, "6~9회": 2.0, "10회이상": 4.9
    },
    "16~18세 고등학생": {
        "모름": 64.8, "앎": 35.2, "미이용": 71.1, "이용": 28.9,
        "경험없음": 67.9, "경험있음": 32.1, "1회": 9.8, "2~3회": 8.0, "4~5회": 5.7, "6~9회": 2.7, "10회이상": 6.0
    }
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

# 4. 메인 화면 레이아웃 분할 및 탭(Tab) 구성
col1, col2 = st.columns([5, 5])

with col1:
    st.subheader(f"📉 [{selected_group}] 실태조사 심층 분석")
    
    tab1, tab2 = st.tabs(["📌 1. 기관 인지 및 이용 실태", "🏠 2. 가정 밖 생활 경험 및 빈도"])
    
    with tab1:
        st.write("여성가족부 실제 데이터에 따르면, 복지 서비스 인지 수준과 실제 이용 경험은 아래와 같이 심각한 불균형을 보이고 있습니다.")
        df_knowledge = pd.DataFrame({
            "구분": ["기관/서비스 모른다", "기관/서비스 안다"],
            "비율(%)": [group_stats["모름"], group_stats["앎"]]
        })
        df_usage = pd.DataFrame({
            "구분": ["이용해본 적 없다", "이용해본 적 있다"],
            "비율(%)": [group_stats["미이용"], group_stats["이용"]]
        })
        
        fig_know = px.bar(df_knowledge, x="구분", y="비율(%)", text="비율(%)", title="복지시설/서비스 인지 여부",
                          color="구분", color_discrete_sequence=["#FF6B6B", "#4D96FF"])
        fig_know.update_traces(texttemplate='%{text}%', textposition='inside')
        st.plotly_chart(fig_know, use_container_width=True)
        
        fig_use = px.bar(df_usage, x="구분", y="비율(%)", text="비율(%)", title="시설/서비스 실제 이용 여부",
                         color="구분", color_discrete_sequence=["#FFD93D", "#6BCB77"])
        fig_use.update_traces(texttemplate='%{text}%', textposition='inside')
        st.plotly_chart(fig_use, use_container_width=True)

    with tab2:
        st.write("청소년들이 가정 밖 생활(가출)을 경험하는 비율과 반복성 빈도 데이터입니다. 위기 청소년 긴급 쉼터의 필요성을 뒷받침합니다.")
        
        df_exp = pd.DataFrame({
            "구분": ["가정 밖 생활 경험 없음", "가정 밖 생활 경험 있음"],
            "비율(%)": [group_stats["경험없음"], group_stats["경험있음"]]
        })
        
        df_freq = pd.DataFrame({
            "빈도": ["1회", "2~3회", "4~5회", "6~9회", "10회 이상"],
            "비율(%)": [group_stats["1회"], group_stats["2~3회"], group_stats["4~5회"], group_stats["6~9회"], group_stats["10회이상"]]
        })
        
        fig_exp = px.pie(df_exp, values="비율(%)", names="구분", title="가정 밖 생활 경험 여부",
                         color_discrete_sequence=["#EFFFFA", "#FF6B6B"], hole=0.4)
        st.plotly_chart(fig_exp, use_container_width=True)
        
        fig_freq = px.bar(df_freq, x="빈도", y="비율(%)", text="비율(%)", title="가정 밖 생활 경험 청소년의 반복 빈도",
                          color="빈도", color_discrete_sequence=px.colors.sequential.Reds_r)
        fig_freq.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig_freq, use_container_width=True)

with col2:
    st.subheader("🔗 위기 유형별 맞춤형 시설 매칭 및 홍보 원클릭 연결")
    st.write("청소년들이 '몰라서 이용하지 못하는' 사각지대를 해소하기 위해 위기 유형별로 즉각적인 법적 근거 중심의 전문 기관 매칭 서비스를 제공합니다.")
    
    crisis =
