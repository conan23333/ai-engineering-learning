def analyzer_log(file_path : str) -> None:
    statistics = {
        "INFO":0,
        "WARNING":0,
        "ERROR":0,
    }
    error_logs=[]
    service_items={}
    try:
        with open(file_path,"r",encoding="utf-8") as log_file:
            for line in log_file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts)!=4:
                    print(f"跳过格式错误的日志：{line}")
                    continue
                timestamp,level,service,message = parts
                pass
                if service in service_items:
                    service_items[service]+=1
                else:
                    service_items[service]=1
                #service_items[service]=service_items.get(service,0) + 1
                if level not in statistics:
                    print(f"未知日志级别：{level}")
                    continue
                if "ERROR" in level:
                    statistics["ERROR"]+=1
                    error_logs.append({
                        "timestamp": timestamp,
                        "level": level,
                        "service": service,
                        "message": message,
                    })
                elif "INFO" in level:
                    statistics["INFO"]+=1
                elif "WARNING" in level:
                    statistics["WARNING"]+=1
                pass
    except FileNotFoundError:
        print(f"找不到日志文件{file_path}")
        return
    print("\n==========日志分析报告=========")
    for level, count in statistics.items():
        print(f"{level}: {count}")
    print("\n====== 错误详情 ======")
    for error in error_logs:
        print(
            f"{error['timestamp']} | "
            f"{error['service']} | "
            f"{error['message']}"
        )
    if(statistics["ERROR"]==0):
        print("正常")
    elif(statistics["ERROR"]<=2):
        print("需要关注")
    else:
        print("严重异常")
    for servicename , count in service_items.items():
        print(f"{servicename}:{count}")
if __name__=="__main__":
    analyzer_log("application.log")