from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import(
    ConfigFileNotFoundError,
    ConfigFormatError,
    ModelAnalysisError,
)

def register_exception_handlers(app):
    @app.exception_handler(ConfigFileNotFoundError)
    async def config_file_not_found(
        request: Request,
        error: ConfigFileNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": str(error),
                "data": None
            },
        )
    @app.exception_handler(ConfigFormatError)
    async def config_format(
        request: Request,
        error: ConfigFormatError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(error),
                "data": None
            },
        )
    @app.exception_handler(ModelAnalysisError)
    async def model_analysis(
        request: Request,
        error: ModelAnalysisError,
    ):
        return JSONResponse(
            status_code=502,
            content={
                "success": False,
                "message": str(error),
                "data": None
            },
        )