import os
from pathlib import Path
from rich import print as rprint

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH, override=True)

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

model = init_chat_model(
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
)
message = [
    {
        "role":"system","content":"你是一个专业的计算机科学老师"
    },
    {
        "role":"user","content":"帮我解释一下什么是向量数据库"
    },
]
# response = model.invoke(message)
# rprint(response)
# print(type(response))

for Sresponse in model.stream(message):
    rprint(Sresponse.text,end="",flush=True)
print(type(Sresponse))
