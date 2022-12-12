from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///../wb-backend/sql_app.db"
DATABASE_URL = "postgresql://nr:nr@localhost:5432/wbv"

engine = create_engine(
    DATABASE_URL
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
base.metadata.create_all(bind=engine)
