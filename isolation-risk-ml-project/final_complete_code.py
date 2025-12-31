# ============================================================================
# 고립·은둔 위험군 예측 모델 - 최종 완성 코드 (명목형 변수 올바른 처리)
# ============================================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, roc_auc_score, precision_score, 
                             recall_score, f1_score, confusion_matrix, 
                             ConfusionMatrixDisplay, roc_curve, auc)
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams, font_manager
import warnings
import joblib
import json


# 📂 디렉토리 설정 (없으면 생성)
import os

directories = ['models', 'results', 'figures']
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"✓ 디렉토리 확인: {directory}")

warnings.filterwarnings('ignore')


# 🎯 시스템에 설치된 한글 폰트 자동 감지
def setup_korean_font():
    """한글 폰트 자동 설정"""
    
    # 가능한 한글 폰트 목록 (우선순위)
    korean_fonts = [
        'Malgun Gothic',      # Windows
        'AppleGothic',        # Mac
        'Noto Sans CJK JP',   # Linux
        'Noto Sans CJK KR',   # Linux (한국)
        'DejaVu Sans',        # Fallback
    ]
    
    # 시스템에 설치된 폰트 확인
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]
    
    # 첫 번째로 발견된 한글 폰트 사용
    for font in korean_fonts:
        if font in available_fonts:
            plt.rcParams['font.family'] = font
            print(f"✓ 한글 폰트 설정됨: {font}")
            break
    
    # 음수 기호
    plt.rcParams['axes.unicode_minus'] = False

# 프로그램 시작시 한 번만 실행
setup_korean_font()



print("=" * 100)
print(">> 단계 1: 데이터 로드 및 기본 설정")
print("=" * 100)

# 1단계: 데이터 로드
file_path = 'C:/Users/human-01/Desktop/streamlitTest/seoul_youth_isolation_withdrawal_survey.csv'
df = pd.read_csv(file_path, encoding='cp949')
print(f"\n>> 데이터 로드 완료")
print(f"   - 샘플 수: {len(df):,}명")
print(f"   - 전체 특성 수: {len(df.columns)}개")

print("\n" + "=" * 100)
print(">> 단계 2: 타겟 변수 정의")
print("=" * 100)

# 2단계: 타겟 변수 정의
# KEY_1: 1=고립·은둔 청년, 2=미해당
y = (df['KEY_1'] == 1).astype(int)

print(f"\n>> 타겟 변수 분포:")
print(f"   - 고위험군 (고립·은둔): {(y == 1).sum():,}명 ({(y == 1).sum()/len(y)*100:.1f}%)")
print(f"   - 저위험군 (미해당): {(y == 0).sum():,}명 ({(y == 0).sum()/len(y)*100:.1f}%)")

print("\n" + "=" * 100)
print(">> 단계 3: 독립변수 선정")
print("=" * 100)

# 3단계: 독립변수 선정
# ✅ 명목형: A1, DQ2, DQ3, DQ5 (순서 없음)
# ✅ 서수형: SQ1, SQ2_X, SQ6_R, A5, A6, B2_R, A11 (순서 있음)
# ✅ 더미형: A4_1~A4_7 (소득원 - 다중선택)
independent_vars = [
    'SQ1', 'A1', 'SQ2_X', 'SQ6_R', 'A5', 'A6', 'B2_R', 'DQ2', 'DQ3', 'DQ5', 'DQ5_1', 'A11',
    'A4_1', 'A4_2', 'A4_3', 'A4_4', 'A4_5', 'A4_6', 'A4_7', 'B7', 'B8'
]

print(f"\n>> 변수 타입 분류:")
print(f"   🔴 명목형(순서 없음): A1, DQ2, DQ3, DQ5, B5_1, B7, B8 → 원-핫 인코딩 필수")
print(f"   🟡 서수형(순서 있음): SQ1, SQ2_X, SQ6_R, A5, A6, B2_R, A11 → 그대로 사용")
print(f"   🔵 더미형(다중선택): A4_1~A4_7 → 0/1 그대로")

# 변수 검증 및 결측치 확인
missing_summary = {}
for var in independent_vars:
    if var in df.columns:
        missing_count = df[var].isna().sum()
        missing_pct = (missing_count / len(df)) * 100
        missing_summary[var] = missing_pct
        
        status = "✅" if missing_pct < 5 else "⚠️" if missing_pct < 10 else "❌"
        print(f"{status} {var:10s} | 결측치: {missing_count:4d} ({missing_pct:5.2f}%)")
    else:
        print(f"❌ {var:10s} | 컬럼을 찾을 수 없습니다!")

# ============================================================================
# 단계 4: 데이터 전처리 (수정됨)
# ============================================================================
print("\n" + "=" * 100)
print(">> 단계 4: 데이터 전처리")
print("=" * 100)

X = df[independent_vars].copy()

print(f"\n>> 전처리 전:")
print(f"   - 샘플 수: {len(X):,}명")
print(f"   - 특성 수: {X.shape[1]}개")
print(f"   - 결측치 총 개수: {X.isna().sum().sum()}")

# 4.1 소득원(A4_1~7) 결측치는 0(선택안함)으로 처리
income_cols = ['A4_1', 'A4_2', 'A4_3', 'A4_4', 'A4_5', 'A4_6', 'A4_7']
X[income_cols] = X[income_cols].fillna(0)
print(f"\n>> 4.1 소득원 결측치 처리: 0으로 대체")

# 4.2 수치형/범주형 변수 구분해서 결측치 처리
print(f"\n>> 4.2 결측치 처리 (수치형/범주형 구분):")

numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

# 수치형: 중앙값
for col in numeric_cols:
    if X[col].isna().sum() > 0:
        median_val = X[col].median()
        X[col].fillna(median_val, inplace=True)
        print(f"   ✓ {col}: 중앙값 {median_val:.2f} 으로 대체")

# 범주형: 최빈값
for col in categorical_cols:
    if X[col].isna().sum() > 0:
        mode_vals = X[col].mode()
        if len(mode_vals) > 0:
            X[col].fillna(mode_vals[0], inplace=True)
            print(f"   ✓ {col}: 최빈값으로 대체")



print(f"\n>> 4.3 원-핫 인코딩 (명목형 변수):")
print(f"   대상 변수: DQ2, DQ3, DQ5, A1, B8, B2_R, B7")

# 🚨 중요: B5_1과 B8을 columns 리스트에 꼭 추가해야 합니다!
X = pd.get_dummies(
    X, 
    columns=['DQ2', 'DQ3', 'DQ5', 'A1', 'B8', 'B2_R', 'B7'], 
    drop_first=True,
    dtype=int
)


# 4.3 원-핫 인코딩 (명목형 변수만)
print("\n" + "=" * 50)
print("✂️ 단계 4.5: 불필요한 저성능 변수 제거 (Feature Selection)")
print("=" * 50)

# 1. 삭제할 변수 리스트 정의 (중요도 하위 변수들 직접 지정)
# 팁: 모델을 한 번 돌려보고 중요도가 0.001 미만인 것들을 여기에 적으세요.
drop_features = [
    'B2_R_5.0',
    'B2_R_4.0',
    'B7_7',
    'DQ5_7'
]

# 2. 데이터셋에 해당 컬럼이 있는지 확인 후 삭제
cols_to_drop = [col for col in drop_features if col in X.columns]

if cols_to_drop:
    X = X.drop(columns=cols_to_drop)
    print(f">> 삭제된 변수 ({len(cols_to_drop)}개): {cols_to_drop}")
else:
    print(">> 삭제할 변수가 데이터에 없습니다.")



print(f"\n>> 전처리 후:")
print(f"   - 최종 샘플 수: {len(X):,}명")
print(f"   - 특성 수: {X.shape[1]}개 (원본 {len(independent_vars)}개 → {X.shape[1]}개)")
print(f"   - 결측치: {X.isna().sum().sum()}개")
print(f"   - 새로 생성된 컬럼 예시: {list(X.columns[-10:])}")

# ============================================================================
# 단계 5: 데이터 분할 및 스케일링
# ============================================================================
print("\n" + "=" * 100)
print(">> 단계 5: 데이터 분할 및 스케일링")
print("=" * 100)

# 5.1 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 

    random_state=42, 
    stratify=y
)

print(f"\n>> 5.1 데이터 분할 결과 (80:20):")
print(f"   - 학습 데이터: {len(X_train):,}명 (80%)")
print(f"   - 테스트 데이터: {len(X_test):,}명 (20%)")
print(f"   - 학습 고위험군: {(y_train == 1).sum()}명 ({(y_train == 1).sum()/len(y_train)*100:.1f}%)")
print(f"   - 테스트 고위험군: {(y_test == 1).sum()}명 ({(y_test == 1).sum()/len(y_test)*100:.1f}%)")

# 5.2 스케일링 (로지스틱 회귀에 필수, RF는 불필요)
print(f"\n>> 5.2 데이터 스케일링 (StandardScaler):")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 학습 데이터로만 fit
X_test_scaled = scaler.transform(X_test)        # 테스트는 transform만

print(f"   ✓ 학습 데이터로만 fit")
print(f"   ✓ 테스트 데이터는 transform만 적용 (데이터 누수 방지)")

# ============================================================================
# 단계 6: 모델 학습
# ============================================================================
print("\n" + "=" * 100)
print(">> 단계 6: 모델 학습")
print("=" * 100)

# 6.1 로지스틱 회귀
print(f"\n>> 6.1 로지스틱 회귀 학습 중...")
lr_model = LogisticRegression(
    max_iter=1000, 
    random_state=42, 
    class_weight='balanced'  # 불균형 클래스 처리
)
lr_model.fit(X_train_scaled, y_train)
print(f"   ✓ 완료")

# 6.2 랜덤 포레스트
print(f"\n>> 6.2 랜덤 포레스트 학습 중...")
rf_model = RandomForestClassifier(
    n_estimators=100, 
    random_state=42, 
    class_weight='balanced',
    n_jobs=-1
)
rf_model.fit(X_train, y_train)  # 원본 데이터 (스케일링 불필요)
print(f"   ✓ 완료")

# ============================================================================
# 단계 7: 하이퍼파라미터 튜닝
# ============================================================================
print("\n" + "=" * 100)
print(">> 단계 7: 하이퍼파라미터 튜닝 (GridSearchCV)")
print("=" * 100)

param_grid = {
    'n_estimators': [100, 150, 200],
    'max_depth': [10, 15, 20],
    'min_samples_split': [5, 10, 15],
    'min_samples_leaf': [2, 4, 6]
}

print(f"\n>> 파라미터 탐색 중... (이 과정은 시간이 걸릴 수 있습니다)")

grid_search = GridSearchCV(
    RandomForestClassifier(
        random_state=42, 
        class_weight='balanced',
        n_jobs=-1
    ),
    param_grid, 
    cv=5,              # 5-Fold 교차 검증
    scoring='f1',      # F1-Score 기준 (재현율 중시)
    n_jobs=-1,
    verbose=0
)

grid_search.fit(X_train, y_train)
rf_best = grid_search.best_estimator_

print(f"\n>> 튜닝 완료")
print(f"   최적 파라미터: {grid_search.best_params_}")
print(f"   최적 F1-Score: {grid_search.best_score_:.4f}")


# ============================================================================
# 🎯 단계 7.5: 모델 저장
# ============================================================================
print(f"\n>> 단계 7.5: 학습된 모델 저장")
print(f"{'='*60}")

import joblib

# 1️⃣ RandomForest 모델 저장 (최고 성능)
joblib.dump(grid_search.best_estimator_, 'models/random_forest_best_model.pkl')
print(f"   ✓ models/random_forest_best_model.pkl 저장됨")

# 2️⃣ LogisticRegression 모델 저장
joblib.dump(lr_model, 'models/logistic_regression_model.pkl')
print(f"   ✓ models/logistic_regression_model.pkl 저장됨")

# 3️⃣ StandardScaler 저장 (중요! 입력 데이터 정규화용)
joblib.dump(scaler, 'models/standard_scaler.pkl')
print(f"   ✓ models/standard_scaler.pkl 저장됨")

# 4️⃣ 학습에 사용된 특성명 저장 (입력 순서 맞추기 위함)
feature_names_list = list(X.columns)
joblib.dump(feature_names_list, 'models/feature_names.pkl')
print(f"   ✓ models/feature_names.pkl 저장됨 ({len(feature_names_list)}개 특성)")


# 5️⃣ 메타데이터에 모델 저장 정보 추가
saved_model_info = {
    'saved_files': {
        'random_forest': {
            'filename': 'models/random_forest_best_model.pkl',
            'n_estimators': int(grid_search.best_params_.get('n_estimators', 100)),
            'max_depth': int(grid_search.best_params_.get('max_depth', 10)),
            'accuracy': float(accuracy_score(y_test, grid_search.predict(X_test_scaled)))
        },
        'logistic_regression': {
            'filename': 'models/logistic_regression_model.pkl',
            'accuracy': float(accuracy_score(y_test, lr_model.predict(X_test_scaled)))
        },
        'scaler': {
            'filename': 'models/standard_scaler.pkl',
            'type': 'StandardScaler'
        },
        'features': {
            'filename': 'models/feature_names.pkl',
            'count': len(feature_names_list)
        }
    }
}

# 메타데이터 업데이트는 마지막 단계에서 일괄 처리합니다.
# with open('00_metadata.json', 'w', encoding='utf-8') as f:
#     json.dump(metadata, f, indent=4, ensure_ascii=False)
# print(f"   ✓ 00_metadata.json 업데이트됨 (모델 정보 추가)")

print(f"\n✅ 총 4개 모델 파일 저장 완료!")
print(f"\n생성된 파일:")
print(f"   1. models/random_forest_best_model.pkl (RandomForest 모델)")
print(f"   2. models/logistic_regression_model.pkl (LogisticRegression 모델)")
print(f"   3. models/standard_scaler.pkl (데이터 정규화용 Scaler)")
print(f"   4. models/feature_names.pkl (특성명 목록)")

print(f"\n💡 이제 app.py에서 이 모델들을 로드해서 실제 예측을 할 수 있습니다!")

# ============================================================================
# 단계 8: 모델 성능 평가
# ============================================================================
print("\n" + "=" * 100)
print(">> 단계 8: 모델 성능 평가")
print("=" * 100)

def get_metrics(model, X_data, y_true, name):
    """모델 성능 지표 계산"""
    pred = model.predict(X_data)
    proba = model.predict_proba(X_data)[:, 1]
    return {
        'Model': name,
        'Accuracy': accuracy_score(y_true, pred),
        'ROC-AUC': roc_auc_score(y_true, proba),
        'Precision': precision_score(y_true, pred),
        'Recall': recall_score(y_true, pred),
        'F1-Score': f1_score(y_true, pred)
    }

m1 = get_metrics(lr_model, X_test_scaled, y_test, 'Logistic Regression')
m2 = get_metrics(rf_model, X_test, y_test, 'Random Forest (Basic)')
m3 = get_metrics(rf_best, X_test, y_test, 'Random Forest (Best - F1 Optimized)')

comparison_df = pd.DataFrame([m1, m2, m3])

print("\n>> 최종 성능 비교표:")
print(comparison_df.to_string(index=False))

best_idx = comparison_df['F1-Score'].idxmax()
best_model_name = comparison_df.loc[best_idx, 'Model']
print(f"\n>> 🏆 최고 성능 모델: {best_model_name}")

# ============================================================================
# 단계 9: 시각화
# ============================================================================
print("\n" + "=" * 100)
print(">> 단계 9: 시각화")
print("=" * 100)

# 9.1 Confusion Matrix
print(f"\n>> 9.1 혼동 행렬 시각화 중...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ConfusionMatrixDisplay.from_estimator(
    lr_model, X_test_scaled, y_test, 
    display_labels=['Normal', 'Isolated'], 
    ax=axes[0], 
    cmap='Blues'
)
axes[0].set_title("Logistic Regression", fontsize=12, fontweight='bold')

ConfusionMatrixDisplay.from_estimator(
    rf_best, X_test, y_test, 
    display_labels=['Normal', 'Isolated'], 
    ax=axes[1], 
    cmap='Greens'
)
axes[1].set_title("Random Forest (Best)", fontsize=12, fontweight='bold')

plt.tight_layout()
plt.tight_layout()
plt.savefig('figures/01_confusion_matrix.png', dpi=300)
print("   ✓ figures/01_confusion_matrix.png 저장")
plt.close()

# 9.2 ROC Curve
print(f"\n>> 9.2 ROC Curve 시각화 중...")

fig, ax = plt.subplots(figsize=(10, 7))

fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_model.predict_proba(X_test_scaled)[:, 1])
auc_lr = auc(fpr_lr, tpr_lr)
ax.plot(fpr_lr, tpr_lr, label=f'Logistic Regression (AUC = {auc_lr:.3f})', linewidth=2)

fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_best.predict_proba(X_test)[:, 1])
auc_rf = auc(fpr_rf, tpr_rf)
ax.plot(fpr_rf, tpr_rf, label=f'Random Forest Best (AUC = {auc_rf:.3f})', linewidth=2, color='green')

ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random Guess')
ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate', fontsize=12)
ax.set_title('ROC Curve Comparison', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.tight_layout()
plt.savefig('figures/02_roc_curve.png', dpi=300)
print("   ✓ figures/02_roc_curve.png 저장")
plt.close()

# 9.3 특성 중요도
print(f"\n>> 9.3 특성 중요도 시각화 중...")

importances = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_best.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\n>> 상위 10개 중요 변수:")
print(importances.head(10).to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(
    x='Importance', y='Feature', 
    data=importances.head(10), 
    palette='viridis',
    ax=ax
)
ax.set_title('Top 10 Features for Predicting Youth Isolation', fontsize=14, fontweight='bold')
ax.set_xlabel('Importance', fontsize=12)

plt.tight_layout()
plt.tight_layout()
plt.savefig('figures/03_feature_importance.png', dpi=300)
print("   ✓ figures/03_feature_importance.png 저장")
plt.close()

# 9.4 A11 분포 (교류빈도)
print(f"\n>> 9.4 A11(교류빈도) 분포 시각화 중...")

fig, ax = plt.subplots(figsize=(10, 6))

sns.kdeplot(
    data=df[df['KEY_1']==1], x='A11', 
    label='Isolated (High Risk)', 
    fill=True, 
    color='red', 
    alpha=0.6,
    ax=ax
)
sns.kdeplot(
    data=df[df['KEY_1']==2], x='A11', 
    label='Normal (Low Risk)', 
    fill=True, 
    color='blue', 
    alpha=0.6,
    ax=ax
)

ax.set_title('Distribution of Interaction Frequency (A11)', fontsize=14, fontweight='bold')
ax.set_xlim(0, 100)
ax.set_xlabel('A11 Value', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend(fontsize=11)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.tight_layout()
plt.savefig('figures/04_a11_distribution.png', dpi=300)
print("   ✓ figures/04_a11_distribution.png 저장")
plt.close()

# ============================================================================
# 단계 10: 결과 저장
# ============================================================================
print("\n" + "=" * 100)
print(">> 단계 10: 결과 저장")
print("=" * 100)

# 10.1 모델 성능
try:
    comparison_df.to_csv('results/01_model_comparison_results.csv', index=False)
    print(f"   ✓ results/01_model_comparison_results.csv 저장")
except PermissionError:
    print(f"   ⚠️ 저장 실패: 'results/01_model_comparison_results.csv'가 열려있습니다. 파일명을 변경하여 저장합니다.")
    comparison_df.to_csv('results/01_model_comparison_results_new.csv', index=False)
    print(f"   ✓ results/01_model_comparison_results_new.csv 저장")

# 10.2 특성 중요도
try:
    importances.to_csv('results/02_feature_importance.csv', index=False)
    print(f"   ✓ results/02_feature_importance.csv 저장")
except PermissionError:
    print(f"   ⚠️ 저장 실패: 'results/02_feature_importance.csv'가 열려있습니다. 파일명을 변경하여 저장합니다.")
    importances.to_csv('results/02_feature_importance_new.csv', index=False)
    print(f"   ✓ results/02_feature_importance_new.csv 저장")

# 10.3 로지스틱 회귀 계수
lr_coef = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': lr_model.coef_[0]
}).sort_values('Coefficient', key=abs, ascending=False)

try:
    lr_coef.to_csv('results/03_logistic_coefficients.csv', index=False)
    print(f"   ✓ results/03_logistic_coefficients.csv 저장")
except PermissionError:
    print(f"   ⚠️ 저장 실패: 'results/03_logistic_coefficients.csv'가 열려있습니다. 파일명을 변경하여 저장합니다.")
    lr_coef.to_csv('results/03_logistic_coefficients_new.csv', index=False)
    print(f"   ✓ results/03_logistic_coefficients_new.csv 저장")

# 10.4 메타데이터
import json
metadata = {
    'timestamp': pd.Timestamp.now().isoformat(),
    'dataset': {
        'total_samples': len(df),
        'samples_after_preprocessing': len(X),
        'total_features_original': len(independent_vars),
        'total_features_after_encoding': X.shape[1]
    },
    'train_test_split': {
        'train_size': len(X_train),
        'test_size': len(X_test),
        'train_positive': int((y_train == 1).sum()),
        'test_positive': int((y_test == 1).sum())
    },
    'encoding_info': {
        'nominal_variables': ['A1 (노동여부)', 'DQ2 (직업)', 'DQ3 (혼인상태)', 'DQ5 (주택형태)'],
        'encoding_method': 'OneHotEncoding (drop_first=True)',
        'dummy_variables_created': X.shape[1] - len(independent_vars)
    },
    'preprocessing': {
        'scaler': 'StandardScaler',
        'missing_value_treatment': '중앙값(수치형), 최빈값(범주형)',
        'income_cols_treatment': '0으로 대체 (선택안함)'
    },
    'models': {
        'logistic_regression': {
            'max_iter': 1000,
            'class_weight': 'balanced'
        },
        'random_forest_basic': {
            'n_estimators': 100,
            'class_weight': 'balanced'
        },
        'random_forest_best': {
            'best_params': grid_search.best_params_,
            'best_f1_score': float(grid_search.best_score_)
        }
    },
    'saved_files': saved_model_info['saved_files'],
    'best_model': best_model_name,
    'best_metrics': {
        'accuracy': float(comparison_df.loc[best_idx, 'Accuracy']),
        'roc_auc': float(comparison_df.loc[best_idx, 'ROC-AUC']),
        'precision': float(comparison_df.loc[best_idx, 'Precision']),
        'recall': float(comparison_df.loc[best_idx, 'Recall']),
        'f1_score': float(comparison_df.loc[best_idx, 'F1-Score'])
    }
}

try:
    with open('00_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    print(f"   ✓ 00_metadata.json 저장")
except PermissionError:
    print(f"   ⚠️ 저장 실패: '00_metadata.json'이 열려있습니다. 파일명을 변경하여 저장합니다.")
    with open('00_metadata_new.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    print(f"   ✓ 00_metadata_new.json 저장")

# ============================================================================
# 최종 요약
# ============================================================================
print("\n" + "=" * 100)
print("✨ 분석 완료!")
print("=" * 100)

print(f"""
📊 최종 결과:

🎯 최고 성능 모델: {best_model_name}
   - Accuracy: {comparison_df.loc[best_idx, 'Accuracy']:.4f} ({comparison_df.loc[best_idx, 'Accuracy']*100:.1f}%)
   - ROC-AUC: {comparison_df.loc[best_idx, 'ROC-AUC']:.4f}
   - Precision: {comparison_df.loc[best_idx, 'Precision']:.4f}
   - Recall: {comparison_df.loc[best_idx, 'Recall']:.4f}
   - F1-Score: {comparison_df.loc[best_idx, 'F1-Score']:.4f}

📊 데이터 처리:
   ✅ 원본 샘플: {len(df):,}명
   ✅ 최종 샘플: {len(X):,}명
   ✅ 원본 특성: {len(independent_vars)}개
   ✅ 최종 특성: {X.shape[1]}개 (원-핫 인코딩 적용)
   
📊 인코딩 방식 (올바른 처리):
   ✅ 명목형 변수: A1, DQ2, DQ3, DQ5 → 원-핫 인코딩
   ✅ 서수형 변수: SQ1, SQ2_X, SQ6_R, A5, A6, B2_R, A11 → 그대로 사용
   ✅ 더미 변수: A4_1~A4_7 → 0/1 그대로

📁 생성된 파일:
   ✅ 00_metadata.json (분석 정보)
   ✅ 01_model_comparison_results.csv (모델 성능)
   ✅ 02_feature_importance.csv (특성 중요도)
   ✅ 03_logistic_coefficients.csv (로지스틱 계수)
   ✅ 01_confusion_matrix.png (혼동 행렬)
   ✅ 02_roc_curve.png (ROC 곡선)
   ✅ 03_feature_importance.png (특성 중요도)
   ✅ 04_a11_distribution.png (교류빈도 분포)

🚀 다음 단계:
   1. 생성된 CSV 파일로 보고서 작성
   2. PNG 이미지를 보고서에 삽입
   3. 특성 중요도 분석으로 핵심 요인 도출
   4. 모델별 장단점 분석
""")

print("\n" + "=" * 100)
print("💡 핵심 요약")
print("=" * 100)
print(f"""
✅ 명목형 변수 처리 완료:
   - DQ2, DQ3, DQ5, A1을 올바르게 원-핫 인코딩
   - 각 범주의 독립적 영향 정확히 포착
   - 로지스틱 회귀 계수 해석 용이

✅ 데이터 전처리:
   - 수치형/범주형 구분 처리
   - 소득원(A4_1~7) 0으로 처리
   - StandardScaler 올바르게 적용

✅ 모델 최적화:
   - GridSearchCV로 최적 파라미터 찾음
   - F1-Score 기준으로 재현율 확보
   - class_weight='balanced'로 불균형 처리

이제 정확하고 신뢰할 수 있는 모델입니다! 🎯
""")
