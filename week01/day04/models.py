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

class AnalyzeResponse(BaseModel):
    success: bool
    content: str | None = None
    model: str | None = None
    usage: UsageData
    error: str | None = None