import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH, override=True)


def analyze_with_model(report: dict) -> dict:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv(
        "DEEPSEEK_BASE_URL",
        "https://api.deepseek.com",
    )
    model = os.getenv(
        "DEEPSEEK_MODEL",
        "deepseek-v4-flash",
    )

    if not api_key:
        return {
            "success": False,
            "error": "未配置DEEPSEEK_API_KEY",
        }

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=60.0,
        max_retries=2,
    )

    report_text = json.dumps(
        report,
        ensure_ascii=False,
        indent=2,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一名严谨的资深运维工程师。"
                        "请分析用户提供的结构化日志报告。\n"
                        "必须遵守以下规则：\n"
                        "1. 将已知事实和可能原因严格分开；\n"
                        "2. 每个可能原因都标注为假设；\n"
                        "3. health_check只表示对应URL可访问，"
                        "不能自动代表业务服务或数据库健康；\n"
                        "4. 不得直接建议重启、扩容或修改生产配置，"
                        "必须先说明需要验证的证据；\n"
                        "5. 信息不足时，明确指出还需要哪些数据；\n"
                        "6. 不得编造报告中不存在的服务依赖关系。\n\n"
                        "请按以下结构输出：\n"
                        "一、已知事实\n"
                        "二、风险判断\n"
                        "三、待验证假设\n"
                        "四、排查步骤\n"
                        "五、安全处理建议\n"
                        "六、缺失信息"
                    ),
                },
                {
                    "role": "user",
                    "content": report_text,
                },
            ],
            temperature=0.2,
            stream=False,
        )

        content = response.choices[0].message.content
        usage = response.usage

        return {
            "success": True,
            "model": response.model,
            "content": content,
            "usage": {
                "prompt_tokens": getattr(
                    usage,
                    "prompt_tokens",
                    None,
                ),
                "completion_tokens": getattr(
                    usage,
                    "completion_tokens",
                    None,
                ),
                "total_tokens": getattr(
                    usage,
                    "total_tokens",
                    None,
                ),
            },
        }

    except OpenAIError as error:
        error_text = str(error)
        status_code = getattr(error, "status_code", None)

        if status_code == 401:
            message = "DeepSeek API Key无效"
        elif status_code == 402:
            message = "DeepSeek账户余额不足"
        elif status_code == 429:
            message = "DeepSeek请求频率过高"
        elif status_code in (500, 503):
            message = "DeepSeek服务暂时异常，请稍后重试"
        else:
            message = error_text

        return {
            "success": False,
            "status_code": status_code,
            "error": message,
            "detail": error_text,
        }