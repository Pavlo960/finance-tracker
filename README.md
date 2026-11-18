<div align="center">

# 💰 Finance Tracker API

**REST API для обліку витрат і доходів з конвертацією гривні за офіційним курсом НБУ**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.162-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.1-D71F00?logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-default-003B57?logo=sqlite&logoColor=white)

</div>

---

## ✨ Можливості

- 📝 **CRUD для транзакцій** — створення, перегляд, часткове оновлення та видалення витрат і доходів
- 🔍 **Фільтрація** за категорією, типом (дохід / витрата) та діапазоном дат
- 📄 **Пагінація** через `limit` / `offset`
- 💱 **Конвертація UAH** в кілька валют одночасно за курсом [НБУ](https://bank.gov.ua/) — на сьогодні або на будь-яку дату
- ⚡ **Асинхронні запити** — курси всіх валют завантажуються паралельно (`asyncio.gather`)
- ✅ **Валідація даних** через Pydantic v2 (точні суми в `Decimal`, без похибок float)
- 📚 **Автоматична документація** Swagger UI та ReDoc

## 🛠 Стек

| Шар | Технологія |
|---|---|
| Веб-фреймворк | FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.x (typed `Mapped`) |
| Валідація | Pydantic v2 |
| База даних | SQLite (або будь-яка інша через `DATABASE_URL`) |
| HTTP-клієнт | httpx (async) |

## 🚀 Швидкий старт

```bash
# 1. Клонувати репозиторій
git clone https://github.com/pavlo960/finance-tracker.git
cd finance-tracker

# 2. Створити віртуальне оточення
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# 3. Встановити залежності
pip install -r requirements.txt

# 4. Запустити сервер
uvicorn app.main:app --reload
```

Після запуску відкрий:

- 🌐 API — http://127.0.0.1:8000
- 📘 Swagger UI — http://127.0.0.1:8000/docs
- 📗 ReDoc — http://127.0.0.1:8000/redoc

### ⚙️ Конфігурація

| Змінна | Опис | За замовчуванням |
|---|---|---|
| `DATABASE_URL` | Рядок підключення SQLAlchemy | `sqlite:///./app.db` |

Таблиці створюються автоматично при старті застосунку.

## 📡 Ендпоінти

### Транзакції — `/expenses`

| Метод | Шлях | Опис |
|:---:|---|---|
| `GET` | `/expenses` | Список транзакцій з фільтрами та пагінацією |
| `GET` | `/expenses/{id}` | Одна транзакція |
| `POST` | `/expenses` | Створити транзакцію |
| `PATCH` | `/expenses/{id}` | Частково оновити транзакцію |
| `DELETE` | `/expenses/{id}` | Видалити транзакцію |

**Параметри запиту для `GET /expenses`:**

| Параметр | Тип | Опис |
|---|---|---|
| `category` | `str` | Фільтр за категорією |
| `is_income` | `bool` | `true` — лише доходи, `false` — лише витрати |
| `date_from` / `date_to` | `date` | Діапазон дат (включно) |
| `limit` | `int` | 1–100, за замовчуванням 10 |
| `offset` | `int` | Зсув, за замовчуванням 0 |

### Фінанси — `/finances`

| Метод | Шлях | Опис |
|:---:|---|---|
| `GET` | `/finances/convert` | Конвертувати суму в гривнях в інші валюти |

| Параметр | Тип | Опис |
|---|---|---|
| `amount` | `Decimal` | Сума в UAH (> 0) |
| `currencies` | `list[str]` | Коди валют ISO 4217, до 10 штук (за замовчуванням `USD`, `EUR`) |
| `on_date` | `date` | Дата курсу (необовʼязково, за замовчуванням — сьогодні) |

## 🧪 Приклади

**Створити витрату:**

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Продукти",
    "category": "food",
    "amount": "450.75",
    "spent_on": "2026-11-18",
    "note": "Сільпо"
  }'
```

```json
{
  "title": "Продукти",
  "category": "food",
  "amount": "450.75",
  "spent_on": "2026-11-18",
  "note": "Сільпо",
  "is_income": false,
  "id": 1
}
```

**Отримати доходи за листопад:**

```bash
curl "http://127.0.0.1:8000/expenses?is_income=true&date_from=2026-11-01&date_to=2026-11-30"
```

**Конвертувати 1000 ₴ у долари, євро та злоті:**

```bash
curl "http://127.0.0.1:8000/finances/convert?amount=1000&currencies=USD&currencies=EUR&currencies=PLN"
```

```json
{
  "amount_uah": "1000",
  "conversions": [
    { "currency": "USD", "amount": "24.10", "rate_uah": "41.4936", "date": "18.11.2026" },
    { "currency": "EUR", "amount": "20.79", "rate_uah": "48.1012", "date": "18.11.2026" },
    { "currency": "PLN", "amount": "88.37", "rate_uah": "11.3162", "date": "18.11.2026" }
  ],
  "took_seconds": 0.31
}
```

> Курси в прикладі ілюстративні — реальні значення повертає API НБУ.

### Коди помилок

| Код | Коли |
|:---:|---|
| `404` | Транзакцію не знайдено / невідомий код валюти |
| `422` | Невалідні дані запиту |
| `502` | API НБУ недоступне |

## 📁 Структура проєкту

```
finance_tracker/
├── app/
│   ├── main.py            # Точка входу, підключення роутерів
│   ├── database.py        # Двигун SQLAlchemy та сесії
│   ├── models.py          # ORM-модель Expense
│   ├── schemas.py         # Pydantic-схеми (Create / Update / Out)
│   ├── routers/
│   │   ├── expenses.py    # CRUD транзакцій
│   │   └── finances.py    # Конвертація валют
│   └── services/
│       └── external.py    # Клієнт API НБУ
├── requirements.txt
└── README.md
```

## 🗂 Модель даних

| Поле | Тип | Опис |
|---|---|---|
| `id` | `int` | Первинний ключ |
| `title` | `str(100)` | Назва |
| `category` | `str(50)` | Категорія |
| `amount` | `Numeric(10, 2)` | Сума (> 0) |
| `spent_on` | `date` | Дата операції |
| `note` | `str(255)?` | Нотатка (необовʼязково) |
| `is_income` | `bool` | `true` — дохід, `false` — витрата |

---

<div align="center">

Made with ❤️ by [pavlo960](https://github.com/pavlo960)

</div>
