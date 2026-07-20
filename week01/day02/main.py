from json_utils import load_json, save_json
from log_analyzer import analyze_log
from http_client import check_service
from pathlib import Path
from model_client import analyze_with_model

BASE_DIR = Path(__file__).resolve().parent
def main() -> None:
    config_path = BASE_DIR / "config.json"
    try:
        config = load_json(config_path)
    except FileNotFoundError:
        print("找不到配置文件：{config_path}")
        return
    except ValueError as error:
        print(f"配置文件不是合法JSON：{error}")
        return
    log_path = BASE_DIR / config["log_file"]
    report_path = BASE_DIR / config["report_file"]
    report = analyze_log(str(log_path))

    if not report["success"]:
        print(report["error"])
        return

    health_check = check_service(config["health_check_url"])
    report["health_check"] = health_check
    print("正在请求模型分析……")

    ai_analysis = analyze_with_model(report)
    report["ai_analysis"] = ai_analysis

    save_json(report, str(report_path))
    if ai_analysis["success"]:
        print("\n========== AI故障分析 ==========")
        print(ai_analysis["content"])

        usage = ai_analysis["usage"]
        print(f"\nToken总量：{usage['total_tokens']}")
    else:
        print(f"模型分析失败：{ai_analysis['error']}")
    print("日志分析完成")
    print(f"系统状态：{report['status']}")
    print(f"错误数量：{report['statistics']['ERROR']}")
    print(f"报告文件：{config['report_file']}")

    if health_check["reachable"]:
        print(
            f"健康检查：HTTP {health_check['status_code']}, "
            f"{health_check['latency_ms']} ms"
        )
    else:
        print(f"健康检查失败：{health_check['error']}")


if __name__ == "__main__":
    main()