from pydantic import BaseModel,Field

class AnalyzeRequest(BaseModel):
    report_file: str=Field(
        min_length=1,
        max_length=255,
        pattern=r"^[^/\\]+\.json$",
        description="需要分析的 JSON 报告文件名",
        examples=["report.json"],
    )

class ExceptionResponse(BaseModel):
    success: bool = False
    message: str
    data: None

class HealthResponse(BaseModel):
    status: str

class UsageData(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None

class AnalyzeData(BaseModel):
    model: str
    content: str
    usage: UsageData

class APIResponse(BaseModel):
    success:bool
    message:str
    data: AnalyzeData | None=None
class AnalysisRecord(BaseModel):
    id: int
    report_file: str
    model: str|None = None
    content: str | None = None
    created_at: str

class HistoryResponse(BaseModel):
    success: bool
    message: str
    data: list[AnalysisRecord]

class AnalysisDetailRecord(BaseModel):
    success: bool
    message: str
    data: AnalysisRecord |None = None