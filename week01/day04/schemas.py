from pydantic import BaseModel,Field,ConfigDict


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    log_file: str = Field(
        min_length=1,
        max_length=255,
        pattern=r"^[^/\\]+\.log$",
        description="logs 目录下需要分析的日志文件名",
        examples=["application.log"],
    )


class ErrorRecord(BaseModel):
    line_number: int
    timestamp: str
    service: str
    message: str
    traceback: list[str]


class InvalidLine(BaseModel):
    line_number: int
    content: str


class UnknownLevel(BaseModel):
    line_number: int
    timestamp: str
    level: str
    service: str
    message: str


class AnalyzeResponse(BaseModel):
    success: bool
    status: str
    statistics: dict[str, int]
    service_statistics: dict[str, int]
    errors: list[ErrorRecord]
    invalid_lines: list[InvalidLine]
    unknown_levels: list[UnknownLevel]


class HealthResponse(BaseModel):
    status: str

class AIAnalyzeResponse(BaseModel):
    success: bool
    file: str
    message: str