from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
def get_health_status(error_count: int) -> str:
    if error_count == 0:
        return "正常"
    if error_count <= 2:
        return "需要关注"
    return "严重异常"

def analyze_log_file(file_path: Path) -> dict:
    statistics={
        "DEBUG" : 0,
        "INFO" : 0,
        "WARNING" : 0,
        "ERROR" : 0,
    }

    service_statistics = {}
    errors = []
    invalid_lines = []
    unknown_levels=[]
    current_error= None
    if not file_path.exists():
        return{
            "success": False,
            "error": f"找不到日志文件：{file_path.name}"
        }
    
    with file_path.open("r",encoding="utf-8") as log_file:
        for line_number,raw_line in enumerate(log_file,start=1):
            line = raw_line.strip("\r\n")

            if not line.strip():
                continue
            parts =line.split("|",maxsplit=3)

            if len(parts)!=4:
                if current_error is not None:
                    current_error["traceback"].append(line)
                else:
                    invalid_lines.append({
                        "line_number": line_number,
                        "content": line,
                    })
                continue

            timestamp, level, service, message = (
                part.strip() for part in parts
            )

            service_statistics[service] = (
                service_statistics.get(service,0)+1
            )

            if level not in statistics:
                unknown_levels.append({
                    "line_number": line_number,
                    "timestamp": timestamp,
                    "level": level,
                    "service": service,
                    "message": message,
                })
                continue

            statistics[level] += 1

            if level=="ERROR":
                error_record={
                "line_number":line_number,
                "timestamp": timestamp,
                "service": service,
                "message": message,
                "traceback": [],
                }
                errors.append(error_record)
                current_error = error_record
    return{
        "success": True,
        "status": get_health_status(statistics["ERROR"]),
        "statistics": statistics,
        "service_statistics": service_statistics,
        "errors": errors,
        "invalid_lines": invalid_lines,
        "unknown_levels": unknown_levels,
    }