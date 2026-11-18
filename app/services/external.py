from datetime import date
from decimal import Decimal

import httpx

NBU_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"


async def get_rate(client: httpx.AsyncClient, currency: str, on_date: date | None = None) -> dict | None:
    # NBU official rate; without a date it returns today's rate
    params = {"valcode": currency.upper(), "json": ""}
    if on_date is not None:
        params["date"] = on_date.strftime("%Y%m%d")

    response = await client.get(NBU_URL, params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        return None
    return {
        "currency": data[0]["cc"],
        # str() first so the float from JSON doesn't leak rounding errors into Decimal
        "rate_uah": Decimal(str(data[0]["rate"])),
        "date": data[0]["exchangedate"],
    }


async def convert_from_uah(
    client: httpx.AsyncClient, amount: Decimal, currency: str, on_date: date | None = None
) -> dict | None:
    rate = await get_rate(client, currency, on_date)
    if rate is None:
        return None
    return {
        "amount_uah": amount,
        "currency": rate["currency"],
        "amount": (amount / rate["rate_uah"]).quantize(Decimal("0.01")),
        "rate_uah": rate["rate_uah"],
        "date": rate["date"],
    }
