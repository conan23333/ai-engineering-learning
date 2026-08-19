import asyncio
import time
from fastapi import APIRouter
router = APIRouter(
    prefix="/api/v1",
    tags=["AI Log Analyzer"],
)

@router.get("/async-test")
async def async_test():
    await asyncio.sleep(2)

    return {
        "success": True,
        "message": "异步等待完成",
    }
sTime = time.perf_counter()
@router.get("/sync-test")
async def sync_test():
    time.sleep(2)
    eTime = time.perf_counter()
    return {
        "success": True,
        "message": "同步等待完成",
        "returnTime": eTime-sTime,
    }