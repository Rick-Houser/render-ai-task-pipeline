from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from openai import OpenAI
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
Base = declarative_base()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    summary = Column(String)
    priority = Column(String)  # e.g., "High", "Medium", "Low"
    embedding = Column(Vector(1536))  # OpenAI embedding dimension

Base.metadata.create_all(engine)

@app.post("/tasks")
def create_task(description: str):
    # Generate summary and priority using OpenAI
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": f"Summarize and prioritize this task: {description}"}])
    summary = response.choices[0].message.content.split("Summary:")[1].split("Priority:")[0].strip()
    priority = response.choices[0].message.content.split("Priority:")[1].strip()
    
    # Generate embedding
    embedding_resp = client.embeddings.create(model="text-embedding-ada-002", input=description)
    embedding = embedding_resp.data[0].embedding
    
    with Session() as session:
        task = Task(description=description, summary=summary, priority=priority, embedding=embedding)
        session.add(task)
        session.commit()
    return {"id": task.id, "summary": summary, "priority": priority}

@app.post("/query")
def query_tasks(question: str):
    # Generate query embedding
    embedding_resp = client.embeddings.create(model="text-embedding-ada-002", input=question)
    query_embedding = embedding_resp.data[0].embedding
    
    with Session() as session:
        # Semantic search using pgvector
        results = session.query(Task).order_by(Task.embedding.cosine_distance(query_embedding)).limit(5).all()
    return [{"description": t.description, "summary": t.summary} for t in results]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)