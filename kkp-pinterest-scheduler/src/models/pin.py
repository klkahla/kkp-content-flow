from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL

Base = declarative_base()

class Pin(Base):
    __tablename__ = 'pins'

    id = Column(Integer, primary_key=True)
    link = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_path = Column(String(255), nullable=False)
    board_id = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)