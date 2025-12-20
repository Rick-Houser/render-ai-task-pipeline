from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    summary = Column(String)
    priority = Column(String)  # e.g., "High", "Medium", "Low"
    embedding = Column(Vector(1536))  # OpenAI embedding dimension