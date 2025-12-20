from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openai import OpenAI
from dotenv import load_dotenv
from .models import Base, Task
from .tasks import process_task_summary
from pydantic import BaseModel
import os

class TaskCreate(BaseModel):
    description: str

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
app = FastAPI()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

Base.metadata.create_all(engine)

@app.post("/tasks")
def create_task(task: TaskCreate):
    description = task.description
    # Generate embedding
    embedding_resp = client.embeddings.create(model="text-embedding-ada-002", input=description)
    embedding = embedding_resp.data[0].embedding
    
    with Session() as session:
        new_task = Task(description=description, summary="", priority="", embedding=embedding)
        session.add(new_task)
        session.commit()
        task_id = new_task.id
    
    # Enqueue async processing
    process_task_summary.delay(task_id)
    
    return {"id": task_id, "message": "Task created, processing in background"}

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_tasks(query: QueryRequest):
    question = query.question
    # Generate query embedding
    embedding_resp = client.embeddings.create(model="text-embedding-ada-002", input=question)
    query_embedding = embedding_resp.data[0].embedding
    
    with Session() as session:
        # Semantic search using pgvector, only tasks with summaries
        results = session.query(Task).filter(Task.summary != "").order_by(Task.embedding.cosine_distance(query_embedding)).limit(5).all()
    return [{"description": t.description, "summary": t.summary} for t in results]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)