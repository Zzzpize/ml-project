import pickle
from typing import Dict

from backend.ml.preprocessor import clean_text
from backend.ml.extractor import extract_serial_number

MODELS_DIR = "models"

# пороги уверенности
EQUIPMENT_THRESHOLD = 0.2
FAILURE_THRESHOLD = 0.2

# слова, при которых ML не имеет смысла
UNKNOWN_KEYWORDS = [
    "терминал",
    "ingenico",
    "эквайринг",
    "pos",
]


class TicketPredictor:
    def __init__(self):
        self._load_models()

    def _load_models(self):
        with open(f"{MODELS_DIR}/equipment_model.pkl", "rb") as f:
            self.equipment_model = pickle.load(f)

        with open(f"{MODELS_DIR}/equipment_vectorizer.pkl", "rb") as f:
            self.equipment_vectorizer = pickle.load(f)

        with open(f"{MODELS_DIR}/failure_model.pkl", "rb") as f:
            self.failure_model = pickle.load(f)

        with open(f"{MODELS_DIR}/failure_vectorizer.pkl", "rb") as f:
            self.failure_vectorizer = pickle.load(f)

    def _has_unknown_keywords(self, text: str) -> bool:
        return any(word in text for word in UNKNOWN_KEYWORDS)

    def _predict_with_confidence(self, model, vectorizer, text, threshold):
        X = vectorizer.transform([text])
        probs = model.predict_proba(X)[0]

        max_prob = probs.max()
        pred_class = model.classes_[probs.argmax()]

        print(f"[CONFIDENCE] {pred_class}: {max_prob:.3f}")

        if max_prob < threshold:
            return "Не определено", max_prob

        return pred_class, max_prob

    def predict(self, subject: str, description: str) -> Dict:
        raw_text = f"{subject} {description}"
        clean = clean_text(raw_text)

        # --- fallback по ключевым словам ---
        if self._has_unknown_keywords(clean):
            equipment = "Не определено"
            failure = "Не определено"
        else:
            equipment, eq_conf = self._predict_with_confidence(
                self.equipment_model,
                self.equipment_vectorizer,
                clean,
                EQUIPMENT_THRESHOLD
            )

            failure, fail_conf = self._predict_with_confidence(
                self.failure_model,
                self.failure_vectorizer,
                clean,
                FAILURE_THRESHOLD
            )

        serial_number = extract_serial_number(raw_text)

        return {
            "equipment": equipment,
            "failure_point": failure,
            "serial_number": serial_number
        }