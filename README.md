<div align="center">

# 💰 Finance Tracker API

**A REST API for tracking expenses and income, with UAH conversion at the official National Bank of Ukraine rate**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.162-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.1-D71F00?logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-default-003B57?logo=sqlite&logoColor=white)

</div>

---

## ✨ Features

- 📝 **Transaction CRUD**: create, read, partially update and delete expenses and income
- 🔍 **Filtering** by category, type (income / expense) and date range
- 📄 **Pagination** via `limit` / `offset`
- 💱 **UAH conversion** into several currencies at once at the [NBU](https://bank.gov.ua/) rate, for today or any past date
- ⚡ **Async requests**: rates for all currencies are fetched in parallel (`asyncio.gather`)
- ✅ **Data validation** with Pydantic v2 (exact amounts as `Decimal`, no float rounding errors)
- 📚 **Auto-generated docs** with Swagger UI and ReDoc

## 🛠 Tech stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.x (typed `Mapped`) |
| Validation | Pydantic v2 |
| Database | SQLite (or any other via `DATABASE_URL`) |
| HTTP client | httpx (async) |

## 🚀 Quick start

```bash
# 1. Clone the repository
git clone https://github.com/pavlo960/finance-tracker.git
cd finance-tracker

# 2. Create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn app.main:app --reload
```

Once it's running, open:

- 🌐 API: http://127.0.0.1:8000
- 📘 Swagger UI: http://127.0.0.1:8000/docs
- 📗 ReDoc: http://127.0.0.1:8000/redoc

### ⚙️ Configuration

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./app.db` |

Tables are created automatically on startup.

## 📡 Endpoints

### Transactions: `/expenses`

| Method | Path | Description |
|:---:|---|---|
| `GET` | `/expenses` | List transactions with filters and pagination |
| `GET` | `/expenses/{id}` | Get a single transaction |
| `POST` | `/expenses` | Create a transaction |
| `PATCH` | `/expenses/{id}` | Partially update a transaction |
| `DELETE` | `/expenses/{id}` | Delete a transaction |

**Query parameters for `GET /expenses`:**

| Parameter | Type | Description |
|---|---|---|
| `category` | `str` | Filter by category |
| `is_income` | `bool` | `true` for income only, `false` for expenses only |
| `date_from` / `date_to` | `date` | Date range (inclusive) |
| `limit` | `int` | 1–100, default 10 |
| `offset` | `int` | Offset, default 0 |

### Finances: `/finances`

| Method | Path | Description |
|:---:|---|---|
| `GET` | `/finances/convert` | Convert an amount in UAH into other currencies |

| Parameter | Type | Description |
|---|---|---|
| `amount` | `Decimal` | Amount in UAH (> 0) |
| `currencies` | `list[str]` | ISO 4217 currency codes, up to 10 (default `USD`, `EUR`) |
| `on_date` | `date` | Rate date (optional, defaults to today) |

## 🧪 Examples

**Create an expense:**

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Groceries",
    "category": "food",
    "amount": "450.75",
    "spent_on": "2026-11-18",
    "note": "Weekly shopping"
  }'
```

```json
{
  "title": "Groceries",
  "category": "food",
  "amount": "450.75",
  "spent_on": "2026-11-18",
  "note": "Weekly shopping",
  "is_income": false,
  "id": 1
}
```

**Get income for November:**

```bash
curl "http://127.0.0.1:8000/expenses?is_income=true&date_from=2026-11-01&date_to=2026-11-30"
```

**Convert ₴1000 into US dollars, euros and złoty:**

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

> The rates in this example are illustrative. Real values come from the NBU API.

### Error codes

| Code | When |
|:---:|---|
| `404` | Transaction not found / unknown currency code |
| `422` | Invalid request data |
| `502` | NBU API is unavailable |

## 📁 Project structure

```
finance_tracker/
├── app/
│   ├── main.py            # Entry point, router registration
│   ├── database.py        # SQLAlchemy engine and sessions
│   ├── models.py          # Expense ORM model
│   ├── schemas.py         # Pydantic schemas (Create / Update / Out)
│   ├── routers/
│   │   ├── expenses.py    # Transaction CRUD
│   │   └── finances.py    # Currency conversion
│   └── services/
│       └── external.py    # NBU API client
├── requirements.txt
└── README.md
```

## 🗂 Data model

| Field | Type | Description |
|---|---|---|
| `id` | `int` | Primary key |
| `title` | `str(100)` | Title |
| `category` | `str(50)` | Category |
| `amount` | `Numeric(10, 2)` | Amount (> 0) |
| `spent_on` | `date` | Transaction date |
| `note` | `str(255)?` | Note (optional) |
| `is_income` | `bool` | `true` for income, `false` for an expense |

---

<div align="center">

Made with ❤️ by [pavlo960](https://github.com/pavlo960)

</div>
