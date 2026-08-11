import json
import os
from pathlib import Path

from dotenv import load_dotenv
import openai
from openai import OpenAI

from exceptions import (
    AuthenticationError,
    ModelRequestError,
    QuotaExceededError,
    RetryExhaustedError,
    TemporaryNetworkError,
)
from logger_config import setup_logger
from retry import run_with_retry

logger = setup_logger(__name__)
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH, override=True)

SYSTEM_PROMPT = """
你是一名严谨的资深运维工程师。
请分析用户提供的结构化日志报告。

必须遵守以下规则：
1. 将已知事实和可能原因严格分开；
2. 每个可能原因都标注为假设；
3. health_check只表示对应URL可访问，不能自动代表业务服务或数据库健康；
4. 不得直接建议重启、扩容或修改生产配置，必须先说明需要验证的证据；
5. 信息不足时，明确指出还需要哪些数据；
6. 不得编造报告中不存在的服务依赖关系。

请按以下结构输出：
一、已知事实
二、风险判断
三、待验证假设
四、排查步骤
五、安全处理建议
六、缺失信息
""".strip()

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
        max_retries=0,
    )

    report_text = json.dumps(
        report,
        ensure_ascii=False,
        indent=2,
    )
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": report_text,
        },
        ]

    def request_once():
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                stream=False,
            )

        except openai.AuthenticationError as error:
            raise AuthenticationError(
                "DeepSeek API Key无效"
            ) from error

        except openai.RateLimitError as error:
            raise TemporaryNetworkError(
                "DeepSeek请求频率过高"
            ) from error

        except (
            openai.APITimeoutError,
            openai.APIConnectionError,
        ) as error:
            raise TemporaryNetworkError(
                "DeepSeek网络连接或请求超时"
            ) from error

        except openai.APIStatusError as error:
            status_code = error.status_code

            if status_code == 402:
                raise QuotaExceededError(
                    "DeepSeek账户余额不足"
                ) from error

            if status_code in (500, 502, 503, 504):
                raise TemporaryNetworkError(
                    f"DeepSeek服务暂时异常，状态码={status_code}"
                ) from error

            raise ModelRequestError(
                f"DeepSeek请求失败，状态码={status_code}"
            ) from error

        except openai.OpenAIError as error:
            raise ModelRequestError(
                f"DeepSeek SDK调用失败：{error}"
            ) from error
    try:
        response = run_with_retry(
            operation=request_once,
            max_attempts=3,
            base_delay=1.0,
            max_delay=8.0,
        )

    except AuthenticationError as error:
        logger.exception("DeepSeek认证失败")
        return {
            "success": False,
            "error": str(error),
        }

    except QuotaExceededError as error:
        logger.exception("DeepSeek余额不足")
        return {
            "success": False,
            "error": str(error),
        }

    except ModelRequestError as error:
        logger.exception("DeepSeek请求参数或响应异常")
        return {
            "success": False,
            "error": str(error),
        }

    except RetryExhaustedError as error:
        logger.exception("DeepSeek临时故障重试耗尽")
        return {
            "success": False,
            "error": str(error),
        }

    content = response.choices[0].message.content
    usage = response.usage

    if not content:
        logger.error("DeepSeek返回内容为空")
        return {
            "success": False,
            "error": "DeepSeek返回内容为空",
        }

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