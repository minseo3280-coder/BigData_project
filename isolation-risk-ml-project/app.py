import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from PIL import Image
import joblib
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 🎯 한글 폰트 설정
# ============================================================================
import matplotlib as mpl
import platform

system = platform.system()
if system == 'Windows':
    mpl.rcParams['font.family'] = 'Malgun Gothic'
elif system == 'Darwin':  # Mac
    mpl.rcParams['font.family'] = 'AppleGothic'
else:  # Linux
    try:
        mpl.rcParams['font.family'] = 'Noto Sans CJK KR'
    except:
        mpl.rcParams['font.family'] = 'DejaVu Sans'

mpl.rcParams['axes.unicode_minus'] = False

# ============================================================================
# 📄 Streamlit 페이지 설정
# ============================================================================
st.set_page_config(
    page_title="고립·은둔 위험군 예측 모델",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 📦 캐시 함수들
# ============================================================================

@st.cache_data
def load_results():
    """분석 결과 파일 로드"""
    try:

        model_comparison = pd.read_csv('results/01_model_comparison_results.csv')
        feature_importance = pd.read_csv('results/02_feature_importance.csv')
        logistic_coef = pd.read_csv('results/03_logistic_coefficients.csv')
        
        with open('00_metadata.json', 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        return {
            'model_comparison': model_comparison,
            'feature_importance': feature_importance,
            'logistic_coef': logistic_coef,
            'metadata': metadata
        }
    except FileNotFoundError as e:
        st.warning(f"⚠️ 분석 파일 로드 실패: {e}")
        return None

@st.cache_data
def load_images():
    """이미지 파일 로드"""
    images = {}
    image_files = {

        'confusion_matrix': 'figures/01_confusion_matrix.png',
        'roc_curve': 'figures/02_roc_curve.png',
        'feature_importance': 'figures/03_feature_importance.png',
        'a11_distribution': 'figures/04_a11_distribution.png'
    }
    
    for key, filename in image_files.items():
        if os.path.exists(filename):
            images[key] = Image.open(filename)
    
    return images

@st.cache_data
def load_data():
    """원본 데이터 로드"""
    try:
        df = pd.read_csv('seoul_youth_isolation_withdrawal_survey.csv', encoding='cp949')
        return df
    except FileNotFoundError:
        return None

@st.cache_resource
def load_models():
    """🤖 학습된 모델 로드 (캐시됨)"""
    try:

        rf_model = joblib.load('models/random_forest_best_model.pkl')
        lr_model = joblib.load('models/logistic_regression_model.pkl')
        scaler = joblib.load('models/standard_scaler.pkl')
        feature_names = joblib.load('models/feature_names.pkl')
        
        return {
            'rf_model': rf_model,
            'lr_model': lr_model,
            'scaler': scaler,
            'feature_names': feature_names
        }
    except FileNotFoundError as e:
        return None

# ============================================================================
# 📥 데이터 및 모델 로드
# ============================================================================

results = load_results()
images = load_images()
df = load_data()
models = load_models()

# 에러 처리
if results is None:
    st.error("❌ 분석 결과 파일을 찾을 수 없습니다!")
    st.info("먼저 final_complete_code.py를 실행하여 결과 파일을 생성해주세요.")
    st.stop()

if models is None:
    st.error("❌ 모델 파일을 찾을 수 없습니다!")
    st.error("""
    다음 파일들이 필요합니다:

    1. models/random_forest_best_model.pkl
    2. models/logistic_regression_model.pkl
    3. models/standard_scaler.pkl
    4. models/feature_names.pkl
    
    먼저 final_complete_code.py를 실행하세요!
    """)
    st.stop()

# ============================================================================
# 🗂️ 사이드바 네비게이션
# ============================================================================

st.sidebar.title("🎯 고립·은둔 위험군 예측")
st.sidebar.divider()

page = st.sidebar.radio(
    "📑 페이지 선택",
    [
        "🏠 홈",
        "🔮 개인 위험도 진단",
        "📈 모델 성능",
        "📊 특성 분석",
        "📸 시각화",
        "💾 데이터 정보",
        "ℹ️ 정보"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

# 메타데이터 표시
metadata = results['metadata']
st.sidebar.info(f"""
### 📊 분석 정보

**데이터:**
- 샘플: {metadata['dataset']['samples_after_preprocessing']:,}명
- 특성: {metadata['dataset']['total_features_after_encoding']}개

**사용 변수:**
- A1 (노동 여부)
- DQ2 (직업)
- A11 (교류 횟수)
- A5 (식사 횟수)
- A6 (사회경제 수준)
- SQ6_R (동거 인원)

**최고 성능:**
- {metadata['best_model']}
- F1: {metadata['best_metrics']['f1_score']:.4f}
""")

# ============================================================================
# 📄 페이지 1: 홈
# ============================================================================

if page == "🏠 홈":
    st.title("🏠 고립·은둔 위험군 예측 모델")
    
    st.markdown("""
    이 대시보드는 **서울시 고립·은둔 청년 데이터**를 기반으로 머신러닝 모델을 통해 
    **고위험군을 예측**하고 **핵심 영향 요인을 분석**합니다.
    """)
    
    st.divider()
    
    # 주요 지표
    st.subheader("📊 주요 지표")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("정확도", f"{max(results['model_comparison']['Accuracy']):.4f}", "Accuracy")
    with col2:
        st.metric("ROC-AUC", f"{max(results['model_comparison']['ROC-AUC']):.4f}", "구분 능력")
    with col3:
        st.metric("정밀도", f"{max(results['model_comparison']['Precision']):.4f}", "Precision")
    with col4:
        st.metric("재현율", f"{max(results['model_comparison']['Recall']):.4f}", "Recall")
    
    st.divider()
    
    # 모델 성능 테이블
    st.subheader("📋 모델 성능 비교")
    comparison_df = results['model_comparison']
    st.dataframe(
        comparison_df.style.format({
            'Accuracy': '{:.4f}',
            'ROC-AUC': '{:.4f}',
            'Precision': '{:.4f}',
            'Recall': '{:.4f}',
            'F1-Score': '{:.4f}'
        }),
        use_container_width=True,
        height=200
    )
    
    st.divider()
    
    # 프로젝트 개요
    st.subheader("📚 프로젝트 개요")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        ### 🎯 목표
        서울시의 **고립·은둔 위험군**을 머신러닝으로 **예측**하고 **영향 요인을 분석**합니다.
        
        ### 📊 데이터
        - **출처:** 서울시 고립·은둔 실태 조사
        - **샘플:** {metadata['dataset']['samples_after_preprocessing']:,}명
        - **특성:** {metadata['dataset']['total_features_after_encoding']}개
        
        ### 🤖 모델
        - **RandomForest (최고 성능)** - 높은 정확도, 특성 중요도 분석
        - **LogisticRegression** - 해석성 우수, 확률 기반 예측
        
        ### 🔍 주요 기능
        - 🔮 **개인 위험도 진단** - 사용자 입력으로 위험도 예측
        - 📈 **모델 성능** - 상세한 성능 비교
        - 📊 **특성 분석** - 핵심 영향 요인 파악
        - 📸 **시각화** - ROC Curve, Confusion Matrix 등
        """)
    
    with col2:
        st.markdown("""
        ### ⚡ 빠른 참조
        
        **타겟 변수:**
        - 🔴 고위험군 (1)
        - 🟢 저위험군 (0)
        
        **평가 지표:**
        - Accuracy
        - ROC-AUC
        - Precision
        - Recall
        - F1-Score
        
        **사용 변수:**
        - A1: 노동 여부
        - DQ2: 직업
        - A11: 교류 횟수
        - A5: 식사 횟수
        - A6: 사회경제 수준
        - SQ6_R: 동거 인원
        """)

# ============================================================================
# 🔮 페이지 2: 개인 위험도 진단
# ============================================================================

elif page == "🔮 개인 위험도 진단":
    st.title("🔮 개인 위험도 진단")
    
    st.markdown("""
    **6가지 주요 정보**를 입력하면 AI가 고립·은둔 위험도를 판정합니다.
    
    - 🟢 **저위험군**: 사회활동이 활발하고 건강한 생활습관
    - 🟡 **중위험군**: 일부 위험 요소 존재 - 개선 필요
    - 🔴 **고위험군**: 사회적 고립 경향이 높음 - 전문가 상담 권장
    """)
    
    st.divider()

    # ============================================================================
    # 👤 입력 섹션 - 디자인 개선!
    # ============================================================================ 
    # 섹션 0: 나이 (SQ2_X)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with st.container(border=True):
        st.markdown("### 📅 **나이 (연령대)**")
        
        sq2_x = st.radio(
            "SQ2_X: 나이 (5세 단위 연령대)",
            options=[1, 2, 3, 4],
            index=1,
            format_func=lambda x: {
                1: "만 19~24세",
                2: "만 25~29세",
                3: "만 30~34세",
                4: "만 35~39세"
            }[x],
            key="sq2x_radio"
        )
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 섹션 1: 경제 활동 (A1, DQ2)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with st.container(border=True):
        st.markdown("### 💼 **경제 활동**")
        col1, col2 = st.columns(2)
        
        with col1:
            a1 = st.selectbox(
                "**A1: 한 주 동안 1시간 이상의 노동 여부**",
                options=[1.0, 2.0, 3.0],
                format_func=lambda x: {
                    1.0: "✅ 일을 하였다",
                    2.0: "🏖️ 휴가 및 일시 휴직 중",
                    3.0: "❌ 일을 하지 않았다"
                }[x],
                key="a1_select"
            )
        
        with col2:
            dq2 = st.selectbox(
                "**DQ2: 현재 직업**",
                options=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                format_func=lambda x: {
                    1.0: "정규직(상용직)",
                    2.0: "임시직(계약직, 파트타이머)",
                    3.0: "일용직",
                    4.0: "종업원이 있는 자영업자",
                    5.0: "종업원이 없는 자영업자",
                    6.0: "무급가족종사자",
                    7.0: "프리랜서",
                    8.0: "학생",
                    9.0: "기타",
                    10.0: "현재 아무런 일을 하고 있지 않음"
                }[x],
                key="dq2_select"
            )
    
    st.markdown("")  # 간격
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 섹션 2: 사회 활동 (A11)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with st.container(border=True):
        st.markdown("### 👥 **사회 활동**")
        
        a11 = st.slider(
            "**A11: 지난 2주 동안 사람들과의 교류 횟수** ⭐",
            min_value=0,
            max_value=100,
            value=20,
            step=5,
            help="실제로 사람을 만난 횟수 (0~100회)",
            key="a11_slider"
        )
        
        col_info = st.columns([3, 1])
        with col_info[1]:
            st.metric("교류 횟수", f"{a11}회", delta="")
    
    st.markdown("")  # 간격
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 섹션 3: 생활 습관 (A5, A6)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with st.container(border=True):
        st.markdown("### 🍽️ **생활 습관**")
        col3, col4 = st.columns(2)
        
        with col3:
            a5 = st.selectbox(
                "**A5: 하루 동안의 식사 횟수**",
                options=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                format_func=lambda x: {
                    1.0: "4끼 이상 🍖🍖🍖",
                    2.0: "3끼 🍖🍖",
                    3.0: "2끼 🍖",
                    4.0: "1끼 ½",
                    5.0: "2~3일 간격 1끼 ⅕",
                    6.0: "거의 먹지 않음 ⚠️"
                }[x],
                key="a5_select"
            )
        
        with col4:
            a6 = st.selectbox(
                "**A6: 자신의 사회경제적 수준**",
                options=[1.0, 2.0, 3.0, 4.0, 5.0],
                format_func=lambda x: {
                    1.0: "매우 부족함 🔴",
                    2.0: "약간 부족함 🟠",
                    3.0: "적정함 🟡",
                    4.0: "약간 여유있음 🟢",
                    5.0: "매우 여유있음 🟢🟢"
                }[x],
                key="a6_select"
            )
    
    st.markdown("")  # 간격
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 섹션 4: 가구 구성 (SQ6_R) - 새로 추가!
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with st.container(border=True):
        st.markdown("### 👨‍👩‍👧‍👦 **가구 구성**")
        
        sq6_r = st.slider(
            "**SQ6_R: 함께 살고 있는 사람 수 (자신 포함)**",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
            help="자신을 포함한 함께 사는 사람의 총 수",
            key="sq6r_slider"
        )
        
        # 시각적 표현
        col_visual = st.columns([3, 1])
        with col_visual[0]:
            # 간단한 시각화
            people_emojis = "👤" * int(sq6_r)
            st.markdown(f"**{people_emojis}** ({sq6_r}명)")
        with col_visual[1]:
            st.metric("동거 인원", f"{sq6_r}명", delta="")
    
    st.divider()
    
    # ============================================================================
    # 🔮 예측 버튼
    # ============================================================================
    
    col_button = st.columns([1, 2, 1])[1]
    predict_button = col_button.button(
        "🔮 위험도 판정하기",
        use_container_width=True,
        type="primary",
        key="predict_btn"
    )
    
    if predict_button:
        st.divider()
        
        # 📋 1단계: 입력값 요약
        st.subheader("📋 입력값 요약")
        
        summary_df = pd.DataFrame({
            '항목': ['나이(연령대)', '노동 여부', '직업', '교류 횟수', '식사 횟수', '사회경제 수준', '동거 인원'],
            '입력값': [
                {1: "만 19~24세", 2: "만 25~29세", 3: "만 30~34세", 4: "만 35~39세"}[sq2_x],
                {1.0: "일을 하였다", 2.0: "휴가/휴직", 3.0: "일하지 않음"}[a1],
                {1.0: "정규직", 2.0: "임시직", 3.0: "일용직", 4.0: "자영(종원)", 
                 5.0: "자영(무종원)", 6.0: "무급가족", 7.0: "프리랜서", 8.0: "학생", 
                 9.0: "기타", 10.0: "무직"}[dq2],
                f"{a11}회",
                {1.0: "4끼 이상", 2.0: "3끼", 3.0: "2끼", 4.0: "1끼", 
                 5.0: "2~3일에 1끼", 6.0: "거의 없음"}[a5],
                {1.0: "매우부족", 2.0: "약간부족", 3.0: "적정", 
                 4.0: "약간여유", 5.0: "매우여유"}[a6],
                f"{sq6_r}명"
            ]
        })
        
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        try:
            # 🤖 2단계: 모델 예측
            st.subheader("🎯 예측 결과")
            
            # 사용자 입력 데이터 생성
            user_input = {
                'SQ2_X': sq2_x,
                'A1': a1,
                'DQ2': dq2,
                'A11': a11,
                'A5': a5,
                'A6': a6,
                'SQ6_R': sq6_r
            }
            
            user_df = pd.DataFrame([user_input])
            
            # ⚠️ 원-핫 인코딩된 특성들을 0으로 채우기
            for feature in models['feature_names']:
                if feature not in user_df.columns:
                    user_df[feature] = 0
            
            # 특성 순서 맞추기
            user_df = user_df[models['feature_names']]
            
            # 스케일링 (로지스틱 회귀용)
            user_df_scaled = models['scaler'].transform(user_df)
            
            # 🏆 RandomForest 모델로 예측 (최고 성능 모델)
            rf_pred = models['rf_model'].predict(user_df)[0]
            rf_proba = models['rf_model'].predict_proba(user_df)[0]
            
            # 로지스틱 회귀로도 예측 (비교용)
            lr_proba = models['lr_model'].predict_proba(user_df_scaled)[0]
            
            # 결과 표시
            col1, col2, col3 = st.columns(3)
            
            with col1:
                risk_pct = rf_proba[1] * 100
                if risk_pct > 50:
                    color = "🔴"
                elif risk_pct > 30:
                    color = "🟡"
                else:
                    color = "🟢"
                
                st.metric(
                    f"{color} 최고 성능 모델 (RF)",
                    f"{risk_pct:.1f}%",
                    "고위험 확률"
                )
            
            with col2:
                lr_pct = lr_proba[1] * 100
                st.metric(
                    "📊 로지스틱 회귀",
                    f"{lr_pct:.1f}%",
                    "고위험 확률"
                )
            
            with col3:
                if rf_proba[1] > 0.5:
                    risk_level = "🔴 고위험"
                    risk_color = "inverse"
                elif rf_proba[1] > 0.3:
                    risk_level = "🟡 중위험"
                    risk_color = "inverse"
                else:
                    risk_level = "🟢 저위험"
                    risk_color = "inverse"
                
                st.metric("최종 판정", risk_level)
            
            st.divider()
            
            # 💡 권고사항
            st.subheader("💡 권고사항 및 해석")
            
            if rf_proba[1] > 0.5:
                st.error(f"""
                ### 🔴 **고위험군** (고위험 확률: {rf_proba[1]*100:.1f}%)
                
                **현재 상태:** 전문 기관 상담이 **필요합니다** 🚨
                
                **권고 사항:**
                - ☎️ 서울시 고립·은둔 관련 부서에 연락하기
                - 👥 가족이나 신뢰할 수 있는 사람과 대화하기
                - 🏥 정신 건강 검진 받기
                - 💼 직업 훈련 또는 상담 프로그램 참여
                - 🌍 사회 복귀 프로그램 정보 수집
                
                **주의:** 이 진단은 의료 전문가의 진단을 대체할 수 없습니다.
                """)
            
            elif rf_proba[1] > 0.3:
                st.warning(f"""
                ### 🟡 **중위험군** (고위험 확률: {rf_proba[1]*100:.1f}%)
                
                **현재 상태:** 생활습관 **개선이 필요**합니다 ⚠️
                
                **권고 사항:**
                - 📞 전문가 상담받기 (선택사항)
                - 👥 사회적 활동 늘리기 (동호회, 봉사 등)
                - 🍽️ 규칙적인 식사하기
                - 😴 충분한 수면 시간 확보 (하루 6~8시간)
                - 💪 신체 활동 증가 (산책, 운동 등)
                - 🎯 작은 목표부터 시작하기
                """)
            
            else:
                st.success(f"""
                ### 🟢 **저위험군** (고위험 확률: {rf_proba[1]*100:.1f}%)
                
                **현재 상태:** 안전합니다 ✅
                
                **현황:**
                - 사회활동이 활발함 👥
                - 건강한 생활습관 유지 💪
                - 대인관계 양호 🤝
                
                **권고 사항:**
                - 현재의 긍정적인 생활습관을 계속 유지하기
                - 정기적인 건강검진 받기
                - 주변사람들과의 관계 지속하기
                - 새로운 활동이나 취미 시도하기
                """)
            
            st.divider()
            
            # 📊 추가 시각화
            st.subheader("📊 위험도 시각화")
            
            fig, ax = plt.subplots(figsize=(10, 3))
            
            risk_categories = ['저위험\n(0~30%)', '중위험\n(30~50%)', '고위험\n(50~100%)']
            risk_ranges = [0.3, 0.2, 0.5]
            colors = ['#00cc00', '#ffaa00', '#ff0000']
            
            # 현재 확률 표시
            current_pct = rf_proba[1]
            
            # 누적 막대 그래프
            left = 0
            for i, (cat, pct, color) in enumerate(zip(risk_categories, risk_ranges, colors)):
                width = pct
                alpha = 0.7 if (left <= current_pct < left + width) else 0.3
                ax.barh(0, width, left=left, height=0.5, color=color, alpha=alpha, label=cat)
                left += width
            
            # 현재 위치 표시
            ax.axvline(current_pct, color='black', linewidth=2, linestyle='--', label=f'현재: {current_pct*100:.1f}%')
            
            ax.set_xlim([0, 1])
            ax.set_ylim([-0.5, 0.5])
            ax.set_xlabel('고위험 확률', fontsize=12)
            ax.set_title('고립·은둔 위험도 평가', fontsize=14, fontweight='bold')
            ax.set_yticks([])
            ax.legend(loc='upper right', fontsize=10)
            ax.grid(axis='x', alpha=0.3)
            
            st.pyplot(fig)
        
        except Exception as e:
            st.error(f"❌ 예측 오류 발생!")
            st.error(f"자세한 오류: {str(e)}")

# ============================================================================
# 📈 페이지 3: 모델 성능
# ============================================================================

elif page == "📈 모델 성능":
    st.title("📈 모델 성능 분석")
    
    st.markdown("학습된 두 모델(로지스틱 회귀, 랜덤 포레스트)의 성능을 비교합니다.")
    
    st.divider()
    
    # 성능 비교표
    st.subheader("📊 모델 성능 비교")
    comparison_df = results['model_comparison']
    
    st.dataframe(
        comparison_df.style.format({
            'Accuracy': '{:.4f}',
            'ROC-AUC': '{:.4f}',
            'Precision': '{:.4f}',
            'Recall': '{:.4f}',
            'F1-Score': '{:.4f}'
        }).highlight_max(subset=['Accuracy', 'ROC-AUC', 'F1-Score']),
        use_container_width=True,
        height=200
    )
    
    st.divider()
    
    # 혼동 행렬
    if 'confusion_matrix' in images:
        st.subheader("🔲 혼동 행렬 (Confusion Matrix)")
        st.image(images['confusion_matrix'], use_container_width=True)
    
    st.divider()
    
    # ROC Curve
    if 'roc_curve' in images:
        st.subheader("📉 ROC 곡선 (ROC Curve)")
        st.image(images['roc_curve'], use_container_width=True)
        st.caption("ROC 곡선은 모델의 분류 능력을 평가합니다. 곡선이 위쪽에 가까울수록 성능이 좋습니다.")

# ============================================================================
# 📊 페이지 4: 특성 분석
# ============================================================================

elif page == "📊 특성 분석":
    st.title("📊 특성 분석")
    
    st.markdown("모델 학습에 사용된 특성들의 중요도와 계수를 분석합니다.")
    
    st.divider()
    
    # 특성 중요도
    st.subheader("🔥 특성 중요도 (Feature Importance)")
    
    feature_importance = results['feature_importance'].head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(feature_importance)), feature_importance['Importance'].values, color='steelblue')
    ax.set_yticks(range(len(feature_importance)))
    ax.set_yticklabels(feature_importance['Feature'].values)
    ax.set_xlabel('중요도', fontsize=11)
    ax.set_title('상위 10개 중요 특성 (RandomForest)', fontsize=13, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    st.pyplot(fig)
    
    with st.expander("📋 상위 10개 특성 상세 정보"):
        st.dataframe(feature_importance, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # 로지스틱 회귀 계수
    st.subheader("📐 로지스틱 회귀 계수 (Coefficients)")
    
    logistic_coef = results['logistic_coef'].head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['red' if x < 0 else 'green' for x in logistic_coef['Coefficient'].values]
    ax.barh(range(len(logistic_coef)), logistic_coef['Coefficient'].values, color=colors)
    ax.set_yticks(range(len(logistic_coef)))
    ax.set_yticklabels(logistic_coef['Feature'].values)
    ax.set_xlabel('계수값', fontsize=11)
    ax.set_title('상위 10개 로지스틱 회귀 계수', fontsize=13, fontweight='bold')
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    st.pyplot(fig)
    
    with st.expander("📋 상위 10개 계수 상세 정보"):
        st.dataframe(logistic_coef, use_container_width=True, hide_index=True)

# ============================================================================
# 📸 페이지 5: 시각화
# ============================================================================

elif page == "📸 시각화":
    st.title("📸 분석 시각화")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔲 혼동 행렬")
        if 'confusion_matrix' in images:
            st.image(images['confusion_matrix'], use_container_width=True)
        else:
            st.warning("이미지를 찾을 수 없습니다.")
    
    with col2:
        st.subheader("📉 ROC 곡선")
        if 'roc_curve' in images:
            st.image(images['roc_curve'], use_container_width=True)
        else:
            st.warning("이미지를 찾을 수 없습니다.")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🔥 특성 중요도")
        if 'feature_importance' in images:
            st.image(images['feature_importance'], use_container_width=True)
        else:
            st.warning("이미지를 찾을 수 없습니다.")
    
    with col4:
        st.subheader("📊 A11 분포")
        if 'a11_distribution' in images:
            st.image(images['a11_distribution'], use_container_width=True)
        else:
            st.warning("이미지를 찾을 수 없습니다.")

# ============================================================================
# 💾 페이지 6: 데이터 정보
# ============================================================================

elif page == "💾 데이터 정보":
    st.title("💾 데이터 정보")
    
    if df is not None:
        st.subheader("📊 데이터 기본 통계")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("샘플 수", f"{len(df):,}")
        with col2:
            st.metric("특성 수", len(df.columns))
        with col3:
            st.metric("결측치", df.isna().sum().sum())
        
        st.divider()
        
        st.subheader("🎯 타겟 변수 분포")
        if 'KEY_1' in df.columns:
            target_counts = df['KEY_1'].value_counts()
            st.write(target_counts)
        
        st.divider()
        
        st.subheader("📈 사용 변수 통계")
        
        for var in ['A1', 'DQ2', 'A11', 'A5', 'A6', 'SQ6_R']:
            if var in df.columns:
                with st.expander(f"📌 {var}"):
                    st.write(df[var].describe())
    else:
        st.warning("데이터를 로드할 수 없습니다.")

# ============================================================================
# ℹ️ 페이지 7: 정보
# ============================================================================

elif page == "ℹ️ 정보":
    st.title("ℹ️ 프로젝트 정보")
    
    st.markdown("""
    ## 📖 개요
    
    이 프로젝트는 **서울시 고립·은둔 청년 실태조사 데이터**를 기반으로 
    머신러닝 모델을 개발하여 **고위험군을 예측**하는 것을 목표합니다.
    
    ## 🎯 목표
    
    - 고립·은둔 위험군을 **조기에 식별**
    - **영향 요인 분석**을 통한 정책 제언
    - **개인 위험도 진단** 도구 제공
    
    ## 📊 데이터
    
    - **출처:** 서울시 고립·은둔 청년 실태조사
    - **샘플:** 5,513명
    - **특성:** 20개 (최종 6개 사용)
    
    ## 🤖 모델
    
    ### 로지스틱 회귀 (Logistic Regression)
    - **장점:** 해석성 우수, 확률 기반 예측
    - **단점:** 선형 결정 경계
    
    ### 랜덤 포레스트 (Random Forest) ⭐ **최고 성능**
    - **장점:** 높은 정확도, 비선형 패턴 포착
    - **단점:** 블랙박스 모델
    
    ## 📈 주요 성능
    
    """)
    
    comparison_df = results['model_comparison']
    st.dataframe(comparison_df, use_container_width=True)
    
    st.markdown(f"""
    
    ## 🔧 기술 스택
    
    - **데이터 처리:** pandas, numpy
    - **머신러닝:** scikit-learn
    - **시각화:** matplotlib, seaborn
    - **웹 앱:** Streamlit
    
    ## 📚 사용 변수
    
    | 변수명 | 설명 | 타입 |
    |--------|------|------|
    | A1 | 노동 여부 | 범주형 |
    | DQ2 | 직업 | 범주형 |
    | A11 | 교류 횟수 | 연속형 |
    | A5 | 식사 횟수 | 범주형 |
    | A6 | 사회경제 수준 | 범주형 |
    | SQ6_R | 동거 인원 | 연속형 |
    
    ## 📌 주의사항
    
    ⚠️ **이 진단은 의료 전문가의 진단을 대체할 수 없습니다.**
    
    고위험으로 판정된 경우, 반드시 전문가의 상담을 받으세요:
    - 서울시 고립·은둔 관련 부서
    - 정신건강의학과 전문의
    - 사회복지 전문가
    
    ## 📞 연락처
    
    자세한 정보는 서울시 공식 홈페이지를 참고하세요.
    
    ---
    
    **마지막 업데이트:** {metadata['timestamp']}
    """)
