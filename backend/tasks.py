from .celery_app import celery_app
from openai import OpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Task
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task
def process_task_summary(task_id: int):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Summarize and prioritize this task: {task.description}"}
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

        task.summary = summary
        task.priority = priority
        db.commit()
    except Exception as e:
        print(f"Error processing task {task_id}: {e}")
    finally:
        db.close()