# backend/ml/train.py

import joblib
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from backend.ml.preprocessor import clean_text
from backend.ml.failure_groups import failure_to_group, FAILURE_GROUPS


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)


def train_equipment_model(df):
    X = df["text"]
    y = df["equipment"]

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
    )

    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
    )

    model.fit(X_vec, y)

    joblib.dump(vectorizer, MODELS_DIR / "equipment_vectorizer.pkl")
    joblib.dump(model, MODELS_DIR / "equipment_model.pkl")


def train_failure_stage1(df):
    df["failure_group"] = df["failure"].apply(failure_to_group)

    X = df["text"]
    y = df["failure_group"]

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
    )

    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
    )

    model.fit(X_vec, y)

    joblib.dump(vectorizer, MODELS_DIR / "failure_group_vectorizer.pkl")
    joblib.dump(model, MODELS_DIR / "failure_group_model.pkl")


def train_failure_stage2(df):
    for group, failures in FAILURE_GROUPS.items():
        subset = df[df["failure"].isin(failures)]

        if len(subset) < 2:
            continue

        if subset["failure"].nunique() < 2:
            print(f"[SKIP] Group '{group}' has only one failure type")
            continue

        X = subset["text"]
        y = subset["failure"]

        vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
        )

        X_vec = vectorizer.fit_transform(X)

        model = LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
        )

        model.fit(X_vec, y)

        joblib.dump(
            vectorizer,
            MODELS_DIR / f"failure_vectorizer_{group}.pkl"
        )
        joblib.dump(
            model,
            MODELS_DIR / f"failure_model_{group}.pkl"
        )


def main():
    df = pd.read_csv("data/raw/final.csv")

    df["text"] = (
        df["Тема"].fillna("") + " " +
        df["Описание"].fillna("")
    ).apply(clean_text)

    df["equipment"] = df["Тип оборудования"]
    df["failure"] = df["Точка отказа"]

    train_equipment_model(df)
    train_failure_stage1(df)
    train_failure_stage2(df)


if __name__ == "__main__":
    main()