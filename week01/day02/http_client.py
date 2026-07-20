import time
import requests


def check_service(url: str) -> dict:
    start_time = time.perf_counter()

    try:
        response = requests.get(url, timeout=10)

        latency_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        return {
            "url": url,
            "reachable": True,
            "status_code": response.status_code,
            "latency_ms": latency_ms,
        }

    except requests.RequestException as error:
        latency_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        return {
            "url": url,
            "reachable": False,
            "status_code": None,
            "latency_ms": latency_ms,
            "error": str(error),
        }