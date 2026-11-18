import asyncio
import time
from datetime import date
from decimal import Decimal

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.services.external import convert_from_uah

router = APIRouter(prefix="/finances", tags=["finances"])


@router.get("/convert")
async def convert(
    amount: Decimal = Query(gt=0, max_digits=12, decimal_places=2),
    currencies: list[str] = Query(default=["USD", "EUR"], max_length=10),
    on_date: date | None = None,
):
    codes = list(dict.fromkeys(code.upper() for code in currencies))
    if any(len(code) != 3 for code in codes):
        raise HTTPException(status_code=422, detail="Currency code must be 3 letters")

    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            results = await asyncio.gather(
                *(convert_from_uah(client, amount, code, on_date) for code in codes)
            )
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="External service is unavailable")

    missing = [code for code, result in zip(codes, results) if result is None]
    if missing:
        raise HTTPException(status_code=404, detail=f"Currency not found: {', '.join(missing)}")

    return {
        "amount_uah": amount,
        "conversions": [
            {key: result[key] for key in ("currency", "amount", "rate_uah", "date")}
            for result in results
        ],
        "took_seconds": round(time.perf_counter() - start, 2),
    }
