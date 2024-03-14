from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

from app.database.database import Base, engine


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    query_time = Column(DateTime, default=datetime.utcnow())
    article = Column(String, nullable=True)
    subscribed = Column(Boolean, default=False)


History.objects = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
