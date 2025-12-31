
# 🎯 청년 고립·은둔 위험군 탐지를 위한 AI 예측 모델 및 의사결정 지원 웹 서비스

> 서울시 실태조사 데이터를 머신러닝으로 분석하여 고위험군을 조기에 탐지하고, 핵심 요인을 규명하는 프로젝트입니다.
> 
> 본 프로젝트는 단순 모델 학습을 넘어, **해석 가능한 분석 결과 + Streamlit 기반 예측 서비스**까지 구현하는 것을 목표로 했습니다.


---

## 📄 상세 프로젝트 수행 보고서
본 프로젝트의 기획 의도, 전처리 과정, 모델링 상세 결과는 아래 PDF에서 확인하실 수 있습니다.


👉 **[청년고립위험군_AI예측서비스_수행보고서.pdf](isolation-risk-ml-project/청년고립위험군_AI예측서비스_수행보고서.pdf)**

---
  
## 🎬 서비스 시연 영상
https://private-user-images.githubusercontent.com/248983211/531126448-4ddea955-a170-46b6-88e4-1d08ede514f1.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjcxNDEzNzIsIm5iZiI6MTc2NzE0MTA3MiwicGF0aCI6Ii8yNDg5ODMyMTEvNTMxMTI2NDQ4LTRkZGVhOTU1LWExNzAtNDZiNi04OGU0LTFkMDhlZGU1MTRmMS5tcDQ_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMjMxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTIzMVQwMDMxMTJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1jYzY0NDgwMmNlMjU4NWIwZGQ2ZDYzZDI5ZTIzM2E1MTk3Mzc2NWVhNWY3YmE5ZDdjZThjNWM3NTk1MDIwNWQyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.fCbzCEzTMdwMIxGpxJUFgdA7nt48lOGX4e8NI-8i_h0

---

## 🛠 기술 스택 (Tech Stack)

### Environment
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

### Data & Machine Learning
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

### Visualization
![Matplotlib](https://img.shields.io/badge/Matplotlib-ffffff?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Seaborn](https://img.shields.io/badge/Seaborn-4458ad?style=for-the-badge&logoColor=white)

### Deployment
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)


---


## 📌 프로젝트 개요

- **목적**: 청년 고립·은둔 위험군(High-Risk Group)을 조기에 발굴하고, 맞춤형 지원을 위한 의사결정 지원 시스템(DSS) 구축
- **데이터**: 서울시 고립·은둔 청년 실태조사 데이터 (5,513명)
- **핵심 기능**:
  1. **개인 위험도 진단**: 7개 핵심 질문으로 실시간 위험 확률 예측
  2. **요인 분석**: 고립에 영향을 미치는 사회·경제적 요인 시각화
  3. **모델 비교**: 해석력(Logistic Regression) vs 성능(Random Forest) 비교 분석

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

- **데이터 출처**: 서울시 고립·은둔 청년 실태조사 (청년조사) [ https://data.seoul.go.kr/dataList/OA-22347/F/1/datasetView.do]
- **데이터 유형**: 설문 기반 정형 데이터
- **분석 단위**: 개인(청년)


### 주요 사용 변수 예시
| 순위 | 변수명 | 중요도 | 해석 |
|:---:|:---|:---:|:---|
| 1️⃣ | **A11 (교류 빈도)** | **0.155** | 타인과의 만남 횟수 ↓ → 고립 위험 ↑ |
| 2️⃣ | **A6 (사회경제 수준)** | **0.145** | 주관적 경제 수준 ↓ → 고립 위험 ↑ |
| 3️⃣ | **A1_3 (노동 여부: 미취업)** | **0.119** | 지난주 일하지 않음 → 사회적 단절 위험 |
| 4️⃣ | **DQ2_10.0 (직업: 무직)** | 0.069 | 현재 아무런 일을 하지 않음 → 고립 위험 ↑ |
| 5️⃣ | A5 (식사 횟수) | 0.063 | 식사 횟수 ↓ (불규칙한 생활) → 고립 위험 ↑ |
| 6️⃣ | **SQ6_R (동거 가구원 수)** | 0.041 | **1인 가구(나홀로) 또는 가족 내 고립 → 위험 ↑** |
| 7️⃣ | SQ2_X (나이) | 0.034 | 특정 연령대(취업준비생 등) → 고립 취약 |
| 8️⃣ | **DQ3_2.0 (혼인 상태: 미혼)** | 0.032 | **미혼 상태(가족 형성 부재) → 정서적 지지 ↓** |
| 9️⃣ | **A4_1 (소득원: 본인 소득)** | 0.030 | **본인 소득 의존도가 높으나 불안정 → 경제적 고립** |
| 🔟 | **DQ5_4 (주거: 아파트)** | 0.021 | **폐쇄적 주거 환경(아파트 등) → 이웃 교류 ↓** |


---

## 📊 데이터 및 전처리 (Data Pipeline)
전체 데이터 중 고립·은둔 청년은 **8.8%**로, 심각한 **클래스 불균형(Imbalance)** 문제가 있었습니다. 이를 해결하기 위해 정교한 전처리를 수행했습니다.

| 단계 | 주요 내용 | 비고 |
|---|---|---|
| **데이터 정제** | 결측치 처리 (수치형: 중앙값, 범주형: 최빈값) | 이상치 영향 최소화 |
| **특성 공학** | 명목형 변수(직업 등) **원-핫 인코딩(One-Hot Encoding)** | 순서 왜곡 방지 |
| **스케일링** | **StandardScaler** 적용 | 데이터 누수 방지를 위해 Train set 기준으로만 fit |
| **불균형 처리** | **Class Weight ('balanced')** 적용 | 소수 클래스(위험군) 가중치 부여 |

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

## 🤖 모델링 및 성과 (Modeling & Performance)

**"정확도(Accuracy)보다 고위험군을 놓치지 않는 재현율(Recall)과 F1-Score에 집중했습니다."**

최종적으로 **Random Forest (F1 Optimized)** 모델을 선정했습니다.

| 모델 | ROC-AUC | F1-Score | 특징 |
|---|---|---|---|
| **Random Forest (Best)** 🏆 | **0.873** | **0.523** | 비선형 패턴 학습, 가장 균형 잡힌 성능 |
| Logistic Regression | 0.846 | 0.379 | 오탐(False Positive)이 많으나 해석력 우수 |

- **최적화**: GridSearchCV를 통해 `n_estimators=150`, `max_depth=20` 등 최적 파라미터 도출
- **성과**: ROC-AUC 0.873 달성으로 우수한 분류 성능 입증

---
## 💡 핵심 분석 결과 (Key Findings)

머신러닝 분석 결과, 고립·은둔은 단순한 성격 문제가 아닌 **구조적 결핍**에서 비롯됨을 확인했습니다.

1. **가장 강력한 신호 = 교류 빈도 (A11)**
   - 타인과의 만남 횟수가 '0'에 수렴할수록 고립 위험이 급격히 증가했습니다.
     
  ### 📉 고립군 vs 비고립군의 교류 빈도(A11) 차이
![A11 Distribution](isolation-risk-ml-project/figures/04_a11_distribution.jpg)
> **해석**: 붉은색(고위험군) 그래프는 교류 빈도가 '0'에 극단적으로 몰려있는 반면, 파란색(일반군)은 넓게 분포합니다. 즉, **"만남이 거의 없는 상태"가 고립을 예측하는 가장 강력한 신호**입니다.

     
2. **경제적 요인의 중요성 (A6, A1)**
   - 주관적 경제 수준(A6)과 노동 여부(A1)가 상위 중요도 변수로 나타났습니다.
3. **직관적 해석**
   - 모델의 Feature Importance 분석 결과, **[교류 빈도 + 경제 수준 + 노동 여부]** 3가지 변수가 전체 예측력의 **약 42%**를 설명합니다.

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
 ┣ 📜 final_complete_code.py      # 데이터 전처리 및 모델 학습 코드
 ┣ 📜 app.py                      # Streamlit 웹 애플리케이션 코드
 ┣ 📜 requirements.txt
 ┣ 📂 models                      # 학습된 모델 파일 (.pkl)
 ┃ ┣ random_forest_best_model.pkl
 ┃ ┣ logistic_regression_model.pkl
 ┃ ┣ standard_scaler.pkl
 ┃ ┗ feature_names.pkl
 ┣ 📂 results                     # 분석 결과 데이터 (.csv)
 ┃ ┣ 01_model_comparison_results.csv
 ┃ ┣ 02_feature_importance.csv
 ┃ ┗ 03_logistic_coefficients.csv
 ┣ 📂 figures                     # 분석 결과 시각화 이미지 (ROC, Confusion Matrix 등)
 ┃ ┣ 01_confusion_matrix.png
 ┃ ┣ 02_roc_curve.png
 ┃ ┗ 03_feature_importance.png
 ┃ ┗ 04_a11_distribution.png
 ┗ 📜 청년고립위험군_AI예측서비스_수행보고서.pdf    #프로젝트 보고서 파일
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

- 시계열 데이터 통합
- 지역 환경·사회 인프라 데이터 결합
- SHAP 기반 설명 가능 AI 적용


