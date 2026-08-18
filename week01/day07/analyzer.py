import json
from pathlib import Path

from exceptions import (
    ConfigFileNotFoundError,
    ConfigFormatError,
    ModelAnalysisError,
)
from logger_config import setup_logger
from model_client import analyze_with_model
from database import save_analysis

logger = setup_logger(__name__)
BASE_DIR = Path(__file__).resolve().parent


def read_json(file_path: str | Path) -> dict[str, object]:
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    except FileNotFoundError as error:
        raise ConfigFileNotFoundError(
            f"JSON文件不存在：{file_path}"
        ) from error

    except json.JSONDecodeError as error:
        raise ConfigFormatError(
            f"JSON格式错误：{file_path}，"
            f"第{error.lineno}行，第{error.colno}列"
        ) from error

def analyze_report(report_file: str | Path) -> dict:
    report = read_json(report_file)
    logger.info(
        "开始读取报告文件 file=%s",
        report_file,
        )
    result = analyze_with_model(report)
    if not result["success"]:
        raise ModelAnalysisError(
            result.get("error","模型分析失败")
        )
    save_analysis(
        report_file = str(report_file),
        model = result.get("model"),
        content = result.get("content"),)
    return result