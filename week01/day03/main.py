import json
from pathlib import Path

from exceptions import (
    ConfigFileNotFoundError,
    ConfigFormatError,
)
from logger_config import setup_logger
from model_client import analyze_with_model


logger = setup_logger(__name__)
BASE_DIR = Path(__file__).resolve().parent


def read_json(file_path: str | Path) -> dict[str, object]:
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        logger.info(
            "JSON文件读取成功，file_path=%s",
            file_path,
        )
        return data

    except FileNotFoundError as error:
        raise ConfigFileNotFoundError(
            f"JSON文件不存在：{file_path}"
        ) from error

    except json.JSONDecodeError as error:
        raise ConfigFormatError(
            f"JSON格式错误：{file_path}，"
            f"第{error.lineno}行，第{error.colno}列"
        ) from error


def main() -> None:
    logger.info("程序开始运行")

    try:
        config = read_json(BASE_DIR / "config.json")
        logger.info(
            "配置加载完成，app_name=%s",
            config.get("app_name"),
        )

        # 读取第二天生成的结构化日志报告
        report = read_json(BASE_DIR / "report.json")

    except ConfigFileNotFoundError:
        logger.exception("必要的JSON文件不存在，程序结束")
        return

    except ConfigFormatError:
        logger.exception("JSON文件格式损坏，程序结束")
        return

    logger.info("开始请求DeepSeek分析日志")

    ai_analysis = analyze_with_model(report)

    if ai_analysis["success"]:
        usage = ai_analysis.get("usage", {})

        logger.info(
            "DeepSeek分析成功，model=%s，tokens=%s",
            ai_analysis.get("model"),
            usage.get("total_tokens"),
        )

        print("\n========== AI故障分析 ==========")
        print(ai_analysis["content"])

    else:
        logger.error(
            "DeepSeek分析失败，error=%s",
            ai_analysis.get("error"),
        )

    logger.info("程序运行结束")


if __name__ == "__main__":
    main()