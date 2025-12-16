# backend/ml/inference.py

import joblib
from pathlib import Path

from backend.ml.preprocessor import clean_text
from backend.ml.extractor import extract_serial_number


class TicketPredictor:
    def __init__(self):
        project_root = Path(__file__).resolve().parents[2]
        models_dir = project_root / "models"

        # Equipment
        self.equipment_vectorizer = joblib.load(
            models_dir / "equipment_vectorizer.pkl"
        )
        self.equipment_model = joblib.load(
            models_dir / "equipment_model.pkl"
        )

        # Failure stage 1
        self.failure_group_vectorizer = joblib.load(
            models_dir / "failure_group_vectorizer.pkl"
        )
        self.failure_group_model = joblib.load(
            models_dir / "failure_group_model.pkl"
        )

        # Failure stage 2 (lazy-loaded)
        self.failure_models = {}
        self.failure_vectorizers = {}

        for path in models_dir.glob("failure_model_*.pkl"):
            group = path.stem.replace("failure_model_", "")
            self.failure_models[group] = joblib.load(path)
            self.failure_vectorizers[group] = joblib.load(
                models_dir / f"failure_vectorizer_{group}.pkl"
            )

    def _predict_with_confidence(self, model, vectorizer, text):
        X = vectorizer.transform([text])
        proba = model.predict_proba(X)[0]
        idx = proba.argmax()
        return model.classes_[idx], float(proba[idx])

    def predict(self, subject: str, description: str) -> dict:
        raw_text = f"{subject} {description}"
        text = clean_text(raw_text)

        equipment, equipment_conf = self._predict_with_confidence(
            self.equipment_model,
            self.equipment_vectorizer,
            text
        )

        group, group_conf = self._predict_with_confidence(
            self.failure_group_model,
            self.failure_group_vectorizer,
            text
        )

        # Stage-2 failure
        if group in self.failure_models:
            failure, failure_conf = self._predict_with_confidence(
                self.failure_models[group],
                self.failure_vectorizers[group],
                text
            )
        else:
            failure = group
            failure_conf = group_conf

        serial_number = extract_serial_number(subject, description)

        return {
            "equipment": equipment,
            "failure_point": failure,
            "serial_number": serial_number,
        }