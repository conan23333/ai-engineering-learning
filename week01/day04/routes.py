from pathlib import Path

from fastapi import APIRouter

from analyzer import analyze_report
from models import AnalyzeRequest, APIResponse, HealthResponse,ExceptionResponse


router = APIRouter(
    prefix="/api/v1",
    tags=["AI Log Analyzer"],
)
BASE_DIR = Path(__file__).resolve().parent


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    return {
        "status": "ok"
    }


@router.post(
    "/analyze",
    response_model=APIResponse,
    responses={
        400: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
        502: {"model": ExceptionResponse},
    }
)
def analyze(request: AnalyzeRequest):
    report_path = BASE_DIR / request.report_file

    result = analyze_report(report_path)

    return {
        "success": True,
        "message": "分析成功",
        "data": result,
    }