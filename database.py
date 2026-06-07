from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings

# 1. connection url
# Format: "<dialect>:///<path>"
SQLALCHEMY_DATABASE_URL = settings.database_url

# 2. The engine - connection pool
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3. sessionLocal - a factory for creating sessions
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base 
class Base(DeclarativeBase):
    pass

# 5. session dependency - bridge to fastAPI
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()