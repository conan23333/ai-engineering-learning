import httpx
from fastapi import APIRouter,HTTPException
router = APIRouter(
    prefix="/api/v1",
    tags=["log-analyzer"],
)

@router.get("/external-test")
async def external_test():
    async with httpx.AsyncClient() as client:
        response =await client.get(
            "https://jsonplaceholder.typicode.com/todos/1"
        )

    return {
        "success": True,
        "status_code": response.status_code,
        "data": response.json()
    }

@router.get("/external-test/{todo_id}")
async def external_test_by_id(todo_id: int):
    async with httpx.AsyncClient(timeout=5) as client:
        response =await client.get(
            f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
        )

    response.raise_for_status()
    return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json()
    }
