service_name="order-api"
server_ip="192.168.1.10"
cpu_usage=72.5
error_count=3
healthy = error_count==0

print(service_name)
print(server_ip)
print(cpu_usage)
print(error_count)
print(healthy)


print("服务名称：" + service_name)
print(f"服务名称：{service_name}" )
print(f"服务ip{server_ip}")
print(f"cpu负载率{cpu_usage}%")
print(f"错误数量{error_count}")


print(f"服务{service_name}运行在{server_ip}" )
print(f"当前cpu使用率为{cpu_usage}%")
print(f"检测到{error_count}个错误")

if error_count==0:
    print("服务运行正常")
elif error_count<=5:
    print("服务存在少量异常")
else:
    print("服务可能发生严重故障")

if cpu_usage<60:
    print("cpu正常")
elif cpu_usage<=80:
    print("需要关注")
else:
    print("严重警告")


logs = [
    "INFO service started",
    "WARNING cpu usage is high",
    "ERROR database connection failed",
    "INFO request completed",
    "ERROR request timeout"
]

for log in logs:
    print(log)


for log in logs:
    if "ERROR" in log:
        print(f"发现错误：{log}")

error_count = 0
info_count=0
warn_count=0

for log in logs:
    if "ERROR" in log:
        error_count += 1
for log in logs:
    if "INFO" in log:
        info_count += 1
for log in logs:
    if "WARN" in log:
        warn_count += 1                

print(f"错误总数：{error_count}")
print(f"普通信息总数：{info_count}")
print(f"警告总数：{warn_count}")



statistics = {
    "INFO": 0,
    "WARNING": 0,
    "ERROR": 0,
}

for log in logs:
    if "INFO" in log:
        statistics["INFO"] += 1
    elif "WARNING" in log:
        statistics["WARNING"] += 1
    elif "ERROR" in log:
        statistics["ERROR"] += 1

print(statistics)
print(statistics["ERROR"])
for level, count in statistics.items():
    print(f"{level}: {count}")

def is_error(log):
    return "ERROR" in log
print(f"1111{is_error(logs[4])}")
def is_error(log: str) -> bool:
    return "ERROR" in log
print(f"2222{is_error(logs[1])}")
def get_status(error_count: int) -> str:
    if error_count == 0:
        return "正常"
    elif error_count <= 5:
        return "需要关注"
    else:
        return "严重异常"
status = get_status(error_count)
print(f"错误数量为{error_count}，{status}")

def get_cpu_status(cpu_usage:float)-> str:
    if cpu_usage<60:
        print(f"当前正常，CPU负载率{cpu_usage}%")
    elif cpu_usage<=80:
        print(f"需要关注，CPU负载率{cpu_usage}%")
    elif cpu_usage<=100:
        print(f"严重警告，CPU负载率{cpu_usage}%")
    else:
        print(f"参数异常，请检查当前CPU状态")
    pass
get_cpu_status(cpu_usage)
get_cpu_status(100)
get_cpu_status(0)
get_cpu_status(1111)