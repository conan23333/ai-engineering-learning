def get_health_status(error_count: int) -> str:
    if error_count == 0:
        return "正常"
    elif error_count <= 2:
        return "需要关注"
    else:
        return "严重异常"


def analyze_log(file_path: str) -> dict:
    statistics = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
    }

    received_by_service = {}
    error_logs = []
    invalid_lines = []
    unknown_levels = []

    try:
        with open(file_path, "r", encoding="utf-8") as log_file:
            for line_number, line in enumerate(log_file, start=1):
                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                if len(parts) != 4:
                    invalid_lines.append({
                        "line_number": line_number,
                        "content": line,
                    })
                    continue

                timestamp, level, service, message = parts

                received_by_service[service] = (
                    received_by_service.get(service, 0) + 1
                )

                if level not in statistics:
                    unknown_levels.append({
                        "line_number": line_number,
                        "level": level,
                        "timestaps": timestamp,
                        "service":service,
                        "message":message,
                    })
                    continue

                statistics[level] += 1

                if level == "ERROR":
                    error_logs.append({
                        "timestamp": timestamp,
                        "service": service,
                        "message": message,
                    })

    except FileNotFoundError:
        return {
            "success": False,
            "error": f"找不到日志文件：{file_path}",
        }

    error_count = statistics["ERROR"]

    return {
        "success": True,
        "status": get_health_status(error_count),
        "statistics": statistics,
        "received_by_service": received_by_service,
        "errors": error_logs,
        "invalid_lines": invalid_lines,
        "unknown_levels": unknown_levels,
    }