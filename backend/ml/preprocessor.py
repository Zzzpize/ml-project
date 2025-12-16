import re
import string


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    # убираем ссылки и почты
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)

    # оставляем цифры (могут быть важны)
    text = re.sub(r"[^\w\s]", " ", text)

    # убираем лишние пробелы
    text = re.sub(r"\s+", " ", text).strip()

    return text