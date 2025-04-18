from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Pin(Base):
    __tablename__ = 'pins'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_path = Column(String(255), nullable=False)
    board = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
engine = create_engine('sqlite:///pinterest.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)