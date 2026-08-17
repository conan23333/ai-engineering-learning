from pathlib import Path

from fastapi import FastAPI

from analyzer import analyze_report

from models import AnalyzeRequest

from exception_handler import register_exception_handlers

from routes import router

from contextlib import asynccontextmanager

from database import init_db

BASE_DIR = Path(__file__).resolve().parent

def analyze(request: AnalyzeRequest):
    report_path=BASE_DIR/request.report_file
    result = analyze_report(report_path)
    return {
        "success":True,
        "message": "分析成功",
        "data": result,
    }

def health():
    return{
        "status": "ok"
    }

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    lifespan=lifespan
)

register_exception_handlers(app)

app.include_router(router)