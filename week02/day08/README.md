# Week02 Day08：异步 HTTP 客户端

## 今天唯一的核心能力

在 FastAPI 的异步路由中，使用 `httpx.AsyncClient`、`async def` 和
`await` 调用另一个 HTTP 服务。

Day07 已经把服务装进 Docker。Day08 继续 AI 后端工程主线，先学习后端
如何等待模型 API 或其他微服务的 HTTP 响应，而不在等待期间阻塞事件循环。

## 最小结构

- `http_client.py`：只负责异步发送 GET 请求、检查 HTTP 状态码并解析 JSON。
- `app.py`：提供 Day08 健康检查，并异步调用运行在 `8001` 端口的 Day07 健康接口。
- `test_http_client.py`：使用内存中的模拟 HTTP 服务测试成功和 503 两种情况，不访问公网。

## 运行

先让 Day07 容器继续监听 Windows 的 `8001` 端口，然后在本目录安装依赖并启动 Day08：

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8002
```

打开：

```text
http://127.0.0.1:8002/docs
```

依次调用：

```text
GET /api/v1/health
GET /api/v1/check-day07
```

第二个接口成功时会返回 Day07 的健康检查结果；停止 Day07 后再调用，应该得到
`502`。这能直观看出“本服务正常”和“下游服务可访问”是两个不同状态。

运行离线测试：

```powershell
python -m pytest -q -p no:cacheprovider
```

## Day08 完成条件

今天先不要继续引入配置框架、连接池生命周期管理或任务队列。能够用自己的话解释
`async def`、`await` 和 `AsyncClient` 各自做什么，并完成上面的成功/失败实验，
Day08 就可以收尾。
