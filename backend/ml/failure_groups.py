# backend/ml/failure_groups.py

FAILURE_GROUPS = {
    "Питание": [
        "Блок питания",
        "Аккумулятор",
    ],
    "Экран": [
        "Матрица",
        "Камера",
    ],
    "Плата": [
        "Материнская плата",
        "SFP модуль",
        "Wi-fi антенна",
    ],
    "Охлаждение": [
        "Вентилятор",
    ],
    "Хранение": [
        "Диск",
        "Диск ",
        "Оперативная память",
    ],
    "Периферия": [
        "Клавиатура",
        "Динамики",
        "Корпус",
        "Jack",
    ],
    "Другое": [
        "Консультация",
        "Сервер",
    ],
}


def failure_to_group(failure: str) -> str:
    for group, failures in FAILURE_GROUPS.items():
        if failure in failures:
            return group
    return "Другое"