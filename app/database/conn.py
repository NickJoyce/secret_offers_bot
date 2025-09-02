from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import SQLALCHEMY_URL

# Оптимизированные настройки для производительности
async_engine = create_async_engine(
    f"{SQLALCHEMY_URL}", 
    echo=False,
    pool_size=20,  # Размер пула соединений
    max_overflow=30,  # Максимальное количество дополнительных соединений
    pool_pre_ping=True,  # Проверка соединений перед использованием
    pool_recycle=3600,  # Пересоздание соединений каждый час
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

