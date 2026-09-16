
from sqlalchemy import create_engine

from model import Base


DATABASE_URL = "sqlite:///database.db"  

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)