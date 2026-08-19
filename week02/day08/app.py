import httpx
from fastapi import FastAPI, HTTPException
from http_client import get_json
from routes import router

DAY07_HEALTH_URL = "http://127.0.0.1:8001/api/v1/health"

app = FastAPI(title="Week02 Day08 Async HTTP Client")


@app.get("/api/v1/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/check-day07")
async def check_day07() -> dict[str, object]:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            data = await get_json(client, DAY07_HEALTH_URL)
    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail="Day07 service request failed",
        ) from error

    return {
        "success": True,
        "data": data,
    }
app.include_router(router)