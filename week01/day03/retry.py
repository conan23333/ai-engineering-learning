import random
import time
from collections.abc import Callable
from typing import TypeVar

from exceptions import RetryableError, RetryExhaustedError
from logger_config import setup_logger


logger = setup_logger(__name__)

T = TypeVar("T")


def run_with_retry(
    operation: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 8.0,
) -> T:
    if max_attempts < 1:
        raise ValueError("max_attempts必须大于等于1")

    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(
                "开始执行操作，attempt=%s/%s",
                attempt,
                max_attempts,
            )
            return operation()

        except RetryableError as error:
            if attempt == max_attempts:
                raise RetryExhaustedError(
                    f"操作重试{max_attempts}次后仍然失败"
                ) from error

            exponential_delay = base_delay * (2 ** (attempt - 1))
            delay = min(exponential_delay, max_delay)
            jitter = random.uniform(0, delay * 0.3)
            actual_delay = min(delay + jitter, max_delay)

            logger.warning(
                "发生临时故障，准备重试，"
                "attempt=%s/%s，delay=%.2f秒，error=%s",
                attempt,
                max_attempts,
                actual_delay,
                error,
            )

            time.sleep(actual_delay)

    raise RuntimeError("程序不应执行到这里")