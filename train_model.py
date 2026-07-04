import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

def train_and_evaluate_models():
    """Dataset එක load කරලා Logistic Regression + XGBoost train කරනවා"""
    
    # 1. Dataset එක load කරන්න
    try:
        df = pd.read_csv('final_dataset.csv')
        print(f"✅ Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")
    except FileNotFoundError:
        print("❌ final_dataset.csv not found! Run merge_dataset.py first.")
        return
    
    # 2. Target (y) සහ Features (X) වෙන් කරන්න
    # 'file_path' column එක feature එකක් නෙවෙයි - ඒක identify කරන්න විතරයි
    # 'is_buggy' තමයි Target Variable එක
    target_column = 'is_buggy'
    
    if target_column not in df.columns:
        print(f"❌ '{target_column}' column not found in dataset!")
        return
    
    X = df.drop(columns=[target_column, 'file_path'], errors='ignore')
    y = df[target_column]
    
    print(f"\n📊 Features: {X.shape[1]} columns")
    print(f"🎯 Target distribution:")
    print(f"   - Not Buggy (0): {(y == 0).sum()}")
    print(f"   - Buggy (1): {(y == 1).sum()}")
    print(f"   - Bug rate: {(y == 1).sum() / len(y) * 100:.2f}%")
    
    # 3. Data Split: 80% Train, 20% Test
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
    print(f"\n📁 Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # 4. Scale features (Logistic Regression සඳහා feature scaling වැදගත්)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # --- Model 1: Logistic Regression (Baseline) ---
    print("\n" + "="*50)
    print("🔹 Training Logistic Regression (Baseline)...")
    
    # Handle class imbalance
    class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
    weight_dict = dict(zip(np.unique(y_train), class_weights))
    
    lr_model = LogisticRegression(class_weight=weight_dict, max_iter=1000, random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    
    y_pred_lr = lr_model.predict(X_test_scaled)
    y_prob_lr = lr_model.predict_proba(X_test_scaled)[:, 1]
    
    # Metrics
    lr_metrics = {
        'Accuracy': accuracy_score(y_test, y_pred_lr),
        'Precision': precision_score(y_test, y_pred_lr, zero_division=0),
        'Recall': recall_score(y_test, y_pred_lr, zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_lr, zero_division=0),
        'ROC-AUC': roc_auc_score(y_test, y_prob_lr)
    }
    
    print(f"   ✅ Accuracy:  {lr_metrics['Accuracy']:.4f}")
    print(f"   ✅ Precision: {lr_metrics['Precision']:.4f}")
    print(f"   ✅ Recall:    {lr_metrics['Recall']:.4f}")
    print(f"   ✅ F1-Score:  {lr_metrics['F1-Score']:.4f}")
    print(f"   ✅ ROC-AUC:   {lr_metrics['ROC-AUC']:.4f}")
    
    # --- Model 2: XGBoost (Main Model) ---
    print("\n" + "="*50)
    print("🔹 Training XGBoost...")
    
    # XGBoost handles missing values well, doesn't strictly need scaling
    # But we'll use scaled data anyway for consistency (or original, XGBoost doesn't care much about scaling)
    # Let's use original (non-scaled) for XGBoost as it handles it well, but to be safe we use scaled
    # Actually, XGBoost is tree-based, so scaling is NOT required. Let's use raw values for XGBoost.
    # However, our features are small counts, so raw values are fine.
    
    # Class weight balance for XGBoost
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    xgb_model.fit(X_train, y_train)  # XGBoost doesn't need scaling
    
    y_pred_xgb = xgb_model.predict(X_test)
    y_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]
    
    xgb_metrics = {
        'Accuracy': accuracy_score(y_test, y_pred_xgb),
        'Precision': precision_score(y_test, y_pred_xgb, zero_division=0),
        'Recall': recall_score(y_test, y_pred_xgb, zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_xgb, zero_division=0),
        'ROC-AUC': roc_auc_score(y_test, y_prob_xgb)
    }
    
    print(f"   ✅ Accuracy:  {xgb_metrics['Accuracy']:.4f}")
    print(f"   ✅ Precision: {xgb_metrics['Precision']:.4f}")
    print(f"   ✅ Recall:    {xgb_metrics['Recall']:.4f}")
    print(f"   ✅ F1-Score:  {xgb_metrics['F1-Score']:.4f}")
    print(f"   ✅ ROC-AUC:   {xgb_metrics['ROC-AUC']:.4f}")
    
    # --- Comparison ---
    print("\n" + "="*50)
    print("📊 Model Comparison Summary:")
    print("Metric           | Logistic Regression | XGBoost")
    print("-" * 50)
    for metric in ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']:
        print(f"{metric:17} | {lr_metrics[metric]:.4f}            | {xgb_metrics[metric]:.4f}")
    
    # --- Feature Importance (XGBoost) ---
    print("\n" + "="*50)
    print("🔍 Top 5 Most Important Features (XGBoost):")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': xgb_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(5).iterrows():
        print(f"   - {row['feature']}: {row['importance']:.4f}")
    
    # --- Confusion Matrix ---
    print("\n" + "="*50)
    print("📉 Confusion Matrix (XGBoost):")
    cm = confusion_matrix(y_test, y_pred_xgb)
    print(f"   True Negatives:  {cm[0][0]}")
    print(f"   False Positives: {cm[0][1]}")
    print(f"   False Negatives: {cm[1][0]}")
    print(f"   True Positives:  {cm[1][1]}")
    
    # Save the trained model for later (Flask backend)
    import joblib
    joblib.dump(xgb_model, 'devinsight_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')  # Save scaler for new predictions
    print("\n💾 Model saved to devinsight_model.pkl")
    print("💾 Scaler saved to scaler.pkl")
    
    return xgb_metrics, lr_metrics

if __name__ == "__main__":
    train_and_evaluate_models()