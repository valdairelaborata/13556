from sqlalchemy import create_engine

from jvvtmodel import Base

 
DATABASE_URL = 'sqlite:///jvvt.db'
engine = create_engine(DATABASE_URL)
 
Base.metadata.create_all(engine)