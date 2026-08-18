from database import get_analysis_records,get_analysis_by_id,del_analysis_by_id
from fastapi import APIRouter
from pathlib import Path
from analyzer import analyze_report
from models import AnalyzeRequest,APIResponse,HealthResponse,ExceptionResponse,HistoryResponse,AnalysisDetailRecord

BASE_DIR = Path(__file__).resolve().parent
router = APIRouter(
    prefix="/api/v1",
    tags=["AI Log Analyzer"],
)
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
@router.get(
    "/analyses",
    response_model=HistoryResponse
)
def get_analyses(limit: int = 20):
        records = get_analysis_records(limit)
        return {
            "success": True,
            "message": "查询成功",
            "data": records,
        }


@router.get(
    "/analyses/{record_id}",
    response_model=AnalysisDetailRecord
)
def get_analyses(record_id: int):
    record = get_analysis_by_id(record_id)
    if record is None:
        return {
            "success": False,
            "message": "无对应记录",
            "data": None,
        }
    else:
        return {
            "success": True,
            "message": "查询成功",
            "data": record,
        }

@router.delete(
     "/analyses/{record_id}"
)
def delete_analysis_record(record_id: int):
     deleted = del_analysis_by_id(record_id)
     if not deleted:
        return {
            "success": False,
            "message": "无对应记录",
            "data": None,
        }
     else:
        return {
            "success": True,
            "message": "删除成功",
            "data": None,
        }
