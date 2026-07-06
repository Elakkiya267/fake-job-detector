"""
retrain.py — Retrains the model using app.py's StructuralFeatureExtractor
so pickle can resolve it at runtime when Flask loads app.py.
Run from project root: py -3 retrain.py
"""
import os, sys, json, pickle, warnings
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, roc_auc_score, confusion_matrix, classification_report)
from scipy.sparse import hstack, csr_matrix

warnings.filterwarnings('ignore')

# Import the extractor from app.py (so pickle resolves 'app.StructuralFeatureExtractor')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from app import StructuralFeatureExtractor

def train():
    print("=" * 55)
    print("  Fake Job Detector v2 -- Training")
    print("=" * 55)

    # Find dataset
    candidates = [
        os.path.join('data', 'labeled_jobs.csv'),
        os.path.join('fake-job-postings-app', 'data', 'labeled_jobs.csv'),
        os.path.join('src', 'data', 'labeled_jobs.csv'),
    ]
    data_path = next((p for p in candidates if os.path.exists(p)), None)
    if not data_path:
        print("ERROR: labeled_jobs.csv not found. Run 'py -3 src/train_data.py' first.")
        sys.exit(1)

    df = pd.read_csv(data_path)
    print(f"\nLoaded {len(df)} samples  [Fake={int((df['label']==1).sum())}  Legit={int((df['label']==0).sum())}]")

    X = df['text'].fillna('').tolist()
    y = df['label'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train/Test split: {len(X_train)} / {len(X_test)}")

    # Build features
    print("\nBuilding feature matrix...")
    tfidf = TfidfVectorizer(ngram_range=(1, 3), max_features=2000, min_df=1,
                             sublinear_tf=True, strip_accents='unicode',
                             token_pattern=r'\b[a-zA-Z]{2,}\b')
    structural = StructuralFeatureExtractor()

    Xtr = hstack([tfidf.fit_transform(X_train), csr_matrix(structural.fit_transform(X_train))])
    Xte = hstack([tfidf.transform(X_test),      csr_matrix(structural.transform(X_test))])
    print(f"Feature matrix: {Xtr.shape}")

    # Train ensemble
    print("\nTraining ensemble (RF + LR + GB)...")
    rf = RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_leaf=2,
                                 class_weight='balanced', random_state=42, n_jobs=-1)
    lr = LogisticRegression(C=1.5, max_iter=500, class_weight='balanced', random_state=42, solver='lbfgs')
    gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)

    model = VotingClassifier(estimators=[('rf', rf), ('lr', lr), ('gb', gb)],
                              voting='soft', weights=[2, 1, 1])
    model.fit(Xtr, y_train)

    # Evaluate
    y_pred = model.predict(Xte)
    y_prob = model.predict_proba(Xte)[:, 1]
    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec  = recall_score(y_test, y_pred)
    f1   = f1_score(y_test, y_pred)
    auc  = roc_auc_score(y_test, y_prob)
    cm   = confusion_matrix(y_test, y_pred)

    print(f"\n--- Results ---")
    print(f"  Accuracy:  {acc*100:.1f}%")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"  ROC-AUC:   {auc:.4f}")
    print(f"  Confusion Matrix: TN={cm[0,0]} FP={cm[0,1]} FN={cm[1,0]} TP={cm[1,1]}")
    print(f"\n{classification_report(y_test, y_pred, target_names=['Legit','Fake'])}")

    # Cross-validation
    print("Running 5-fold CV...")
    X_all = hstack([tfidf.transform(X), csr_matrix(structural.transform(X))])
    cv    = cross_val_score(model, X_all, y, cv=5, scoring='f1', n_jobs=-1)
    print(f"  CV F1: {cv.mean():.4f} +/- {cv.std():.4f}")

    # Save model
    os.makedirs('models', exist_ok=True)
    bundle = {
        'model':      model,
        'vectorizer': tfidf,
        'structural': structural,
        'classes':    [0, 1],
        'version':    '2.0',
        'trained_at': datetime.now().isoformat(),
    }
    pkl_path = os.path.join('models', 'fake_job_detector.pkl')
    with open(pkl_path, 'wb') as f:
        pickle.dump(bundle, f)
    print(f"\nModel saved -> {pkl_path}")

    # Save metrics
    metrics = {
        'timestamp': datetime.now().isoformat(),
        'model_type': 'Ensemble (RandomForest + LogisticRegression + GradientBoosting)',
        'vectorizer': 'TF-IDF (1-3 grams, 2000 features) + 21 Structural Features',
        'total_samples': len(df),
        'train_samples': len(X_train),
        'test_samples':  len(X_test),
        'fake_samples':  int((df['label'] == 1).sum()),
        'legit_samples': int((df['label'] == 0).sum()),
        'accuracy':  round(acc,  4),
        'precision': round(prec, 4),
        'recall':    round(rec,  4),
        'f1_score':  round(f1,   4),
        'roc_auc':   round(auc,  4),
        'cv_f1_mean': round(float(cv.mean()), 4),
        'cv_f1_std':  round(float(cv.std()),  4),
        'true_positives':  int(cm[1, 1]),
        'true_negatives':  int(cm[0, 0]),
        'false_positives': int(cm[0, 1]),
        'false_negatives': int(cm[1, 0]),
    }
    with open(os.path.join('models', 'training_metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)
    print("Metrics saved -> models/training_metrics.json")
    print("\nDone! Model is ready.")

if __name__ == '__main__':
    train()
