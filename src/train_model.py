"""
train_model.py — Train a Random Forest + TF-IDF fake job detector.
Saves model to: ../models/fake_job_detector.pkl
Saves metrics to: ../models/training_metrics.json
"""

import os, sys, json, pickle, re, warnings
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack, csr_matrix

warnings.filterwarnings('ignore')


# ─── Custom Feature Extractor ──────────────────────────────────────────────────

class StructuralFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Extracts hand-crafted features beyond TF-IDF to capture structural patterns.
    """
    RED_FLAG_PHRASES = [
        r'bank details?', r'bank account', r'account number', r'ifsc',
        r'registration fee', r'training fee', r'joining fee', r'security deposit',
        r'pay upfront', r'pay first', r'advance payment',
        r'western union', r'wire transfer', r'send money',
        r'no experience (is )?required', r'no prior experience',
        r'instant hire', r'hired today', r'start today', r'start immediately',
        r'@gmail\.com', r'@yahoo\.com', r'@hotmail\.com', r'@outlook\.com',
        r'guaranteed income', r'earn thousands', r'easy money', r'get rich',
        r'unmatched earning potential',
        r'data entry.{0,30}(per month|monthly|weekly)',
        r'typing (work|job).{0,30}(per month|monthly)',
        r'envelope stuffing', r'form filling', r'copy paste work',
        r'100% work from home', r'work from anywhere',
        r'limited seats', r'hurry', r'act now', r'today only',
        r'reply with.{0,30}(bank|account|details)',
    ]
    LEGIT_PHRASES = [
        r'pvt\.?\s*ltd', r'private limited', r'llp', r'incorporated',
        r'b\.?tech', r'm\.?tech', r'mba', r'bachelor', r'master', r'degree',
        r'\d+.{0,5}years?.{0,10}experience',
        r'lpa\b', r'ctc\b', r'per annum',
        r'interview', r'technical round', r'hr round', r'selection process',
        r'@[a-z]+\.(com|in|org|net)\b',  # any domain email
        r'python|java|javascript|react|sql|aws|docker|kubernetes',
        r'figma|photoshop|autocad|tableau|power bi|salesforce|hubspot',
    ]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        for text in X:
            t  = text.lower()
            features.append(self._extract(text, t))
        return np.array(features, dtype=np.float32)

    def _extract(self, text, tl):
        words = text.split()
        sentences = re.split(r'[.!?]', text)

        # Red flag count
        red_count = sum(1 for p in self.RED_FLAG_PHRASES if re.search(p, tl))
        # Legit signal count
        legit_count = sum(1 for p in self.LEGIT_PHRASES if re.search(p, tl))

        # Basic stats
        char_len   = len(text)
        word_count = len(words)
        avg_word   = np.mean([len(w) for w in words]) if words else 0
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        exclaim    = text.count('!')
        question   = text.count('?')

        # Email type
        has_personal_email  = int(bool(re.search(r'@(gmail|yahoo|hotmail|outlook|rediffmail)\.', tl)))
        has_corporate_email = int(bool(re.search(r'@(?!(gmail|yahoo|hotmail|outlook|rediffmail))[a-z0-9.\-]+\.(com|in|org|net)', tl)))

        # Salary signals
        has_monthly_salary  = int(bool(re.search(r'[\d,]+\s*per month', tl)))
        has_lpa_salary      = int(bool(re.search(r'[\d.]+\s*(lpa|ctc|per annum)', tl)))
        # High salary + no experience
        no_exp = int(bool(re.search(r'no (prior |previous )?(experience|exp)', tl)))
        high_salary_num = 0
        m = re.search(r'([\d,]+)\s*(per month|/month)', tl)
        if m:
            try:
                high_salary_num = int(m.group(1).replace(',', ''))
            except ValueError:
                pass
        scam_salary_flag = int(no_exp == 1 and high_salary_num >= 50000)

        # Structure
        has_requirements  = int(bool(re.search(r'(requirements?|qualifications?)\s*:', tl)))
        has_responsibilities = int(bool(re.search(r'responsibilities\s*:', tl)))
        has_years_exp     = int(bool(re.search(r'\d+[\+\-]?\s*years? (of\s+)?(experience|exp)', tl)))
        has_interview     = int(bool(re.search(r'(interview|technical round|selection process)', tl)))

        # Urgency
        urgency_count = len(re.findall(r'\b(urgent|immediate|asap|hurry|instant|limited seats|today only|act now)\b', tl))

        # Data entry / typing / scam job titles
        is_scam_title = int(bool(re.search(r'\b(data entry|typing work|copy paste|form fill|envelope stuff|sms sending)\b', tl)))

        return [
            red_count, legit_count,
            char_len, word_count, avg_word,
            caps_ratio, exclaim, question,
            has_personal_email, has_corporate_email,
            has_monthly_salary, has_lpa_salary, scam_salary_flag,
            no_exp, high_salary_num / 100000.0,
            has_requirements, has_responsibilities, has_years_exp, has_interview,
            urgency_count, is_scam_title,
        ]


# ─── Training ─────────────────────────────────────────────────────────────────

def train():
    print("=" * 60)
    print("  Fake Job Detector — Model Training")
    print("=" * 60)

    # ── Load data ──────────────────────────────────────────────────────────────
    # Look for CSV in common locations relative to project root
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    candidates = [
        os.path.join(project_root, 'data', 'labeled_jobs.csv'),
        os.path.join(project_root, 'fake-job-postings-app', 'data', 'labeled_jobs.csv'),
        os.path.join(script_dir, 'data', 'labeled_jobs.csv'),
    ]
    data_path = next((p for p in candidates if os.path.exists(p)), None)
    if data_path is None:
        print("ERROR: labeled_jobs.csv not found. Run 'py -3 src/train_data.py' first.")
        sys.exit(1)

    df = pd.read_csv(data_path)
    print(f"\nLoaded {len(df)} samples.")
    print(f"  Fake (1):  {(df['label'] == 1).sum()}")
    print(f"  Legit (0): {(df['label'] == 0).sum()}")

    X = df['text'].fillna('').tolist()
    y = df['label'].values

    # ── Train / Test split ────────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nSplit: {len(X_train)} train / {len(X_test)} test")

    # ── Build feature matrix ──────────────────────────────────────────────────
    print("\nBuilding features...")
    tfidf = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=2000,
        min_df=1,
        sublinear_tf=True,
        strip_accents='unicode',
        analyzer='word',
        token_pattern=r'\b[a-zA-Z]{2,}\b'
    )
    structural = StructuralFeatureExtractor()

    tfidf_train = tfidf.fit_transform(X_train)
    tfidf_test  = tfidf.transform(X_test)

    struct_train = structural.fit_transform(X_train)
    struct_test  = structural.transform(X_test)

    X_train_final = hstack([tfidf_train, csr_matrix(struct_train)])
    X_test_final  = hstack([tfidf_test,  csr_matrix(struct_test)])

    print(f"Feature matrix shape: {X_train_final.shape}")

    # ── Train ensemble model ──────────────────────────────────────────────────
    print("\nTraining model...")
    rf  = RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_leaf=2,
                                  class_weight='balanced', random_state=42, n_jobs=-1)
    lr  = LogisticRegression(C=1.5, max_iter=500, class_weight='balanced', random_state=42)
    gb  = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)

    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('lr', lr), ('gb', gb)],
        voting='soft',
        weights=[2, 1, 1]      # RF gets highest weight
    )

    ensemble.fit(X_train_final, y_train)

    # ── Evaluate ──────────────────────────────────────────────────────────────
    print("\nEvaluating...")
    y_pred      = ensemble.predict(X_test_final)
    y_pred_prob = ensemble.predict_proba(X_test_final)[:, 1]

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec  = recall_score(y_test, y_pred)
    f1   = f1_score(y_test, y_pred)
    auc  = roc_auc_score(y_test, y_pred_prob)
    cm   = confusion_matrix(y_test, y_pred)

    print(f"\n{'':->40}")
    print(f"  Accuracy:   {acc:.4f}  ({acc*100:.1f}%)")
    print(f"  Precision:  {prec:.4f}")
    print(f"  Recall:     {rec:.4f}")
    print(f"  F1 Score:   {f1:.4f}")
    print(f"  ROC-AUC:    {auc:.4f}")
    print(f"\n  Confusion Matrix:")
    print(f"    TN={cm[0,0]}  FP={cm[0,1]}")
    print(f"    FN={cm[1,0]}  TP={cm[1,1]}")
    print(f"{'':->40}")
    print(f"\n{classification_report(y_test, y_pred, target_names=['Legit','Fake'])}")

    # 5-fold CV
    print("Running 5-fold cross-validation...")
    X_all_final = hstack([tfidf.transform(X), csr_matrix(structural.transform(X))])
    cv_scores = cross_val_score(ensemble, X_all_final, y, cv=5, scoring='f1', n_jobs=-1)
    print(f"  CV F1: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # ── Save model ────────────────────────────────────────────────────────────
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    models_dir = os.path.abspath(models_dir)
    os.makedirs(models_dir, exist_ok=True)

    model_bundle = {
        'model':      ensemble,
        'vectorizer': tfidf,
        'structural': structural,
        'classes':    [0, 1],       # 0=legit, 1=fake
        'version':    '2.0',
        'trained_at': datetime.now().isoformat(),
    }
    pkl_path = os.path.join(models_dir, 'fake_job_detector.pkl')
    with open(pkl_path, 'wb') as f:
        pickle.dump(model_bundle, f)
    print(f"\nModel saved to: {pkl_path}")

    # ── Save metrics ──────────────────────────────────────────────────────────
    metrics = {
        'timestamp':     datetime.now().isoformat(),
        'model_type':    'Ensemble (RandomForest + LogisticRegression + GradientBoosting)',
        'vectorizer':    'TF-IDF (1-3 grams) + Structural Features',
        'total_samples': len(df),
        'train_samples': len(X_train),
        'test_samples':  len(X_test),
        'fake_samples':  int((df['label'] == 1).sum()),
        'legit_samples': int((df['label'] == 0).sum()),
        'accuracy':      round(acc,  4),
        'precision':     round(prec, 4),
        'recall':        round(rec,  4),
        'f1_score':      round(f1,   4),
        'roc_auc':       round(auc,  4),
        'cv_f1_mean':    round(float(cv_scores.mean()), 4),
        'cv_f1_std':     round(float(cv_scores.std()),  4),
        'true_positives':  int(cm[1, 1]),
        'true_negatives':  int(cm[0, 0]),
        'false_positives': int(cm[0, 1]),
        'false_negatives': int(cm[1, 0]),
        'tfidf_features':  2000,
        'structural_features': 21,
    }
    metrics_path = os.path.join(models_dir, 'training_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to: {metrics_path}")
    print("\nTraining complete!")


if __name__ == '__main__':
    train()
