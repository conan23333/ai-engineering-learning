from routes import router
from fastapi import FastAPI
from exceptions import register_exception_handlers
app = FastAPI(title="Week02 Day08 Async HTTP Client")
register_exception_handlers(app)
app.include_router(router)