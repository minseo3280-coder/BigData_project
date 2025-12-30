# 🎯 청년 고립·은둔 위험군 예측 모델  
### 머신러닝 기반 사회적 고립 조기 탐지 시스템

청년의 **인구통계 정보, 생활 습관, 사회적·심리적 상태**를 기반으로  
**고립·은둔 위험군 여부를 예측**하고, 어떤 요인이 청년을 고립 상태로 내모는지 **정량적으로 분석**하는 머신러닝 프로젝트입니다.
본 프로젝트는 단순 모델 학습을 넘어, **해석 가능한 분석 결과 + Streamlit 기반 예측 서비스**까지 구현하는 것을 목표로 했습니다.

---

## 📌 프로젝트 개요

- **프로젝트명**: 청년 고립·은둔 위험군 예측 모델 및 핵심 요인 분석
- **개발 목적**:
  - 고립·은둔 위험 청년 조기 발견
  - 사회적·개인적 결핍 요인 규명
- **개발 형태**: 개인 프로젝트
- **개발 기간**: 2025.01
- **활용 시나리오**:
  - 지자체 청년 고립 예방 서비스
  - 상담·복지 대상자 우선 선별
  - 고립 위험도 체크리스트 자동화

---

## 📢 문제 정의

- **문제 유형**: 이진 분류 (Binary Classification)
- **Target 변수**:
  - `1`: 고립·은둔 위험군
  - `0`: 일반군

### 핵심 질문
> “어떤 사회적·개인적 결핍이  
> 청년을 고립·은둔 상태로 이끄는 가장 강력한 신호인가?”

---

## 📊 데이터 설명

- **데이터 출처**: 서울시 고립·은둔 청년 실태조사 (청년조사)
- **데이터 유형**: 설문 기반 정형 데이터
- **분석 단위**: 개인(청년)

### 주요 사용 변수 예시
| 구분 | 변수 설명 |
|---|---|
| 인구통계 | 연령대 |
| 가구 특성 | 동거 인원 수 |
| 경제 상태 | 노동 여부, 직업 상태 |
| 생활 습관 | 식사 빈도 |
| 사회적 교류 | 최근 사회적 교류 횟수 |
| 주관적 인식 | 사회경제 수준 |

---

## 🛠 기술 스택

### Machine Learning
- Python
- scikit-learn
- pandas / numpy

### Visualization & Analysis
- matplotlib
- seaborn

### Deployment
- Streamlit
- joblib

### 기타
- Git / GitHub

---

## 🤖 사용 모델

### 1️⃣ Logistic Regression
- 이진 분류에 적합한 기본 모델
- 각 변수의 영향 방향(위험 증가/감소) 해석 가능
- 정책·서비스 설명을 위한 해석 중심 모델

### 2️⃣ Random Forest
- 비선형 관계 및 변수 간 상호작용 학습
- 높은 예측 성능
- 최종 예측 서비스에 사용한 모델

> 본 프로젝트에서는 **Random Forest를 최종 서비스 모델로 채택**하고,  
> Logistic Regression은 **해석 및 요인 분석용 모델**로 병행 활용했습니다.

---

## 📈 모델 성능 비교

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression | xx.xx | xx.xx |
| Random Forest | **xx.xx** | **xx.xx** |

---

## 📊 결과 시각화

- Confusion Matrix
- ROC Curve (모델 성능 비교)
- Random Forest Feature Importance
- Logistic Regression Coefficient 분석

이를 통해 **고립·은둔 위험에 영향을 미치는 핵심 요인**을 도출하였습니다.

---

## 🔮 Streamlit 예측 서비스

### 주요 기능
- 사용자 입력 기반 **실시간 고립·은둔 위험도 예측**
- Random Forest & Logistic Regression 확률 비교
- 주요 위험 요인 시각화
- 비개발자도 활용 가능한 웹 UI

### 입력 항목
- 연령대
- 노동 여부
- 직업 상태
- 사회적 교류 횟수
- 식사 빈도
- 사회경제 수준
- 동거 인원 수

---

## 📂 프로젝트 구조

```bash
📦 isolation-risk-ml-project
 ┣ 📜 final_complete_code.py      # 데이터 전처리 및 모델 학습
 ┣ 📜 app.py                      # Streamlit 예측 서비스
 ┣ 📜 requirements.txt
 ┣ 📂 models
 ┃ ┣ random_forest_best_model.pkl
 ┃ ┣ logistic_regression_model.pkl
 ┃ ┣ standard_scaler.pkl
 ┃ ┗ feature_names.pkl
 ┣ 📂 results
 ┃ ┣ 01_model_comparison_results.csv
 ┃ ┣ 02_feature_importance.csv
 ┃ ┗ 03_logistic_coefficients.csv
 ┣ 📂 figures
 ┃ ┣ 01_confusion_matrix.png
 ┃ ┣ 02_roc_curve.png
 ┃ ┗ 03_feature_importance.png
 ┗ 📜 README.md
```
---

## ⚙ 실행 방법

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 1️⃣ 모델 학습 및 결과 생성
python final_complete_code.py

# 2️⃣ Streamlit 앱 실행
streamlit run app.py
```
---
## 💡 프로젝트 차별점

- 예측에 그치지 않고 **해석 가능한 모델 설계**
- 두 모델(Logistic Regression / Random Forest) 비교를 통한 신뢰성 확보
- 분석 결과를 **Streamlit 웹 서비스로 구현**
- 정책·복지 도메인에 바로 적용 가능한 구조

---
## 📎 향후 개선 방향

- 시계열 데이터 확장
- 외부 데이터(지역 환경, 사회 인프라) 결합
- SHAP 기반 설명 가능 AI 적용

