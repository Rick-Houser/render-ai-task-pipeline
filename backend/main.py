from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openai import OpenAI
from dotenv import load_dotenv
from .models import Base, Task
from pydantic import BaseModel
import os

class TaskCreate(BaseModel):
    description: str

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
print("Environment loaded")
app = FastAPI()
print("FastAPI app created")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = create_engine(os.getenv("DATABASE_URL"))
print("Database engine created")
Session = sessionmaker(bind=engine)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("OpenAI client created")

Base.metadata.create_all(engine)
print("Database tables created")

@app.post("/tasks")
def create_task(task: TaskCreate):
    description = task.description
    # Generate embedding
    embedding_resp = client.embeddings.create(model="text-embedding-ada-002", input=description)
    embedding = embedding_resp.data[0].embedding

    # Generate AI summary and priority synchronously
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Summarize and prioritize this task: {description}"}
        ]
    )
    content = response.choices[0].message.content

    # Parse summary and priority
    try:
        summary = content.split("Summary:")[1].split("Priority:")[0].strip()
        priority = content.split("Priority:")[1].strip()
    except:
        summary = content
        priority = "Medium"

    with Session() as session:
        new_task = Task(description=description, summary=summary, priority=priority, embedding=embedding)
        session.add(new_task)
        session.commit()
        task_id = new_task.id

    return {"id": task_id, "message": "Task created with AI summary", "summary": summary, "priority": priority}

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