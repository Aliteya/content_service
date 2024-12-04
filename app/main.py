from fastapi import FastAPI
from app.database import init_db, close_db_connections
from .controllers import user_router, project_router, payment_router, file_router, history_router, render_router

app = FastAPI()
app.include_router(user_router)
app.include_router(project_router)
app.include_router(payment_router)
app.include_router(file_router)
app.include_router(history_router)
app.include_router(render_router)

@app.on_event("startup")
async def startup_event():
    await init_db()
    print("Приложение запущено!")

@app.on_event("shutdown")
async def shutdown_event():

    print("Завершаем фоновые задачи...")
    await close_db_connections()
