from pathlib import Path

from fastapi import FastAPI,HTTPException

from analyzer import analyze_report

from models import AnalyzeRequest, AnalyzeResponse ,HealthResponse,APIResponse

from exception_handler import register_exception_handlers

from routes import router

app = FastAPI()

app.include_router(router)

BASE_DIR = Path(__file__).resolve().parent

@app.post(
    "/analyze",
    response_model=APIResponse,
)
def analyze(request: AnalyzeRequest):
    report_path=BASE_DIR/request.report_file
    result = analyze_report(report_path)
    return {
        "success":True,
        "message": "分析成功",
        "data": result,
    }

@app.get(
    "/healthCheck",
    response_model=HealthResponse,
    )
def health():
    return{
        "status": "ok"
    }

register_exception_handlers(app)