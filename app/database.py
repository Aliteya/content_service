from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .core import Settings
from .models import Base

settings = Settings()

# Настраиваем движок
postgre_database = settings.get_url()
print(postgre_database)

engine = create_async_engine(postgre_database, echo=True)

# Создаём асинхронную фабрику сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session():
    async with AsyncSessionLocal() as session: 
        print("--------------------------------------------", type(session) ,"------------------------------------")
        yield session 

async def init_db():
    print("Инициализация базы данных")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db_connections():
    try:
        await engine.dispose()
        print("Соединения с базой данных успешно закрыты!")
    except Exception as e:
        print(f"Ошибка при закрытии соединений: {e}")
