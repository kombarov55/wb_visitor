from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import app_config

# DATABASE_URL = "sqlite:///{}".format(app_config.db_path)
DATABASE_URL = "postgresql://wb:wb@localhost:5432/wbv"

engine = create_engine(
    DATABASE_URL
)

# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )


session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
base.metadata.create_all(bind=engine)
