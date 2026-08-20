import httpx
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(httpx.HTTPStatusError)
    async def http_status_error_handler(
        request: Request,
        exc: httpx.HTTPStatusError,
    ):
        return JSONResponse(
            status_code=exc.response.status_code,
            content={
                "success":False,
                "message": "请求失败",
            },
        )
    @app.exception_handler(httpx.TimeoutException)
    async def time_out_error_handler(
        request: Request,
        exc: httpx.TimeoutException,
    ):
        return JSONResponse(
            status_code=504,
            content={
                "success":False,
                "message": "外部 API 请求超时",
            },
        )
