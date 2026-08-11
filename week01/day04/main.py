from fastapi import FastAPI,HTTPException
from pathlib import Path
from services.log_service import analyze_log_file
from schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    HealthResponse,
    AIAnalyzeResponse,
)

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR=BASE_DIR/"logs"
app = FastAPI(
    title="AI Log Analyzer",
    description="AI日志故障分析服务",
    version="1.0.0",
)

@app.get("/health",response_model=HealthResponse,)
def health_check():
    return {
        "status":"ok"
    }

@app.post("/api/v1/analyze",response_model=AnalyzeResponse,)
def analyze_log_api(request:AnalyzeRequest):
    log_path = (LOG_DIR/request.log_file).resolve()
    log_dir = LOG_DIR.resolve()
    if log_dir not in log_path.parents:
        raise HTTPException(
            status_code=400,
            detail="日志路径不合法",
        )
    result = analyze_log_file(
        log_path
    )

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )
    return result

@app.post(
    "/api/v1/analyze/ai",
    response_model=AIAnalyzeResponse,
)
def analyze_log_with_ai_api(request: AnalyzeRequest):
    return {
        "success": True,
        "file": request.log_file,
        "message": "已收到 AI 日志分析请求",
    }