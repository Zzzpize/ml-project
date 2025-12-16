import os
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from backend.ml.preprocessor import clean_text

DATA_PATH = "data/raw/train_data.csv"
MODELS_DIR = "models"


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    df["text"] = df["Тема"].fillna("") + " " + df["Описание"].fillna("")
    df["clean_text"] = df["text"].apply(clean_text)

    X = df["clean_text"]
    y_equipment = df["Тип оборудования"]
    y_failure = df["Точка отказа"]

    # ======== SPLIT ========
    X_train_eq, X_test_eq, y_train_eq, y_test_eq = train_test_split(
        X, y_equipment, test_size=0.2, random_state=42, stratify=y_equipment
    )

    X_train_fail, X_test_fail, y_train_fail, y_test_fail = train_test_split(
        X, y_failure, test_size=0.2, random_state=42
    )


    # ======== EQUIPMENT MODEL ========
    equipment_vectorizer = TfidfVectorizer(max_features=15000, ngram_range=(1, 2))
    X_train_eq_vec = equipment_vectorizer.fit_transform(X_train_eq)
    X_test_eq_vec = equipment_vectorizer.transform(X_test_eq)

    equipment_model = LogisticRegression(max_iter=1000, n_jobs=-1)
    equipment_model.fit(X_train_eq_vec, y_train_eq)

    eq_preds = equipment_model.predict(X_test_eq_vec)
    print("\nEquipment model evaluation:")
    print(f"Accuracy: {accuracy_score(y_test_eq, eq_preds):.3f}")
    print(confusion_matrix(y_test_eq, eq_preds))
    print(classification_report(y_test_eq, eq_preds))

    # ======== FAILURE MODEL ========
    failure_vectorizer = TfidfVectorizer(max_features=15000, ngram_range=(1, 2))
    X_train_fail_vec = failure_vectorizer.fit_transform(X_train_fail)
    X_test_fail_vec = failure_vectorizer.transform(X_test_fail)

    failure_model = LogisticRegression(max_iter=1000, n_jobs=-1)
    failure_model.fit(X_train_fail_vec, y_train_fail)

    fail_preds = failure_model.predict(X_test_fail_vec)
    print("\nFailure model evaluation:")
    print(f"Accuracy: {accuracy_score(y_test_fail, fail_preds):.3f}")
    print(confusion_matrix(y_test_fail, fail_preds))
    print(classification_report(y_test_fail, fail_preds))

    # ======== SAVE ========
    with open(f"{MODELS_DIR}/equipment_model.pkl", "wb") as f:
        pickle.dump(equipment_model, f)

    with open(f"{MODELS_DIR}/equipment_vectorizer.pkl", "wb") as f:
        pickle.dump(equipment_vectorizer, f)

    with open(f"{MODELS_DIR}/failure_model.pkl", "wb") as f:
        pickle.dump(failure_model, f)

    with open(f"{MODELS_DIR}/failure_vectorizer.pkl", "wb") as f:
        pickle.dump(failure_vectorizer, f)


if __name__ == "__main__":
    main()