import xgboost as xgb
import numpy as np

# Dummy dataset
X_train = np.array([
    [45, 27.5, 1, 1],   # age, BMI, smoking, family history
    [30, 22.0, 0, 0],
    [50, 29.0, 1, 1]
])
y_train = np.array([1, 0, 1])  # 1 = high risk, 0 = low risk

# Train once
model = xgb.XGBClassifier(eval_metric="logloss")
model.fit(X_train, y_train)

def predict_risk(patient_data: list):
    X_test = np.array([patient_data])
    risk = model.predict_proba(X_test)[0][1]
    return float(risk)
