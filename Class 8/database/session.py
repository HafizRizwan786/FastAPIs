from sqlalchemy import create_engine
from sqlmodel import SQLModel,Session
from typing import Annotated
from fastapi import Depends
from .models import Shipment

engine=create_engine(
    url="sqlite:///Class 8/sqlite.db",
    echo=True,
    connect_args={"check_same_thread":False}
)


def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)
    
    
def get_session():
    with Session(bind=engine) as session:
        yield session
        
SessionDep=Annotated[Session,Depends(get_session)]