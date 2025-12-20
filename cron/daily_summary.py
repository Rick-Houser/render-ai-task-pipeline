from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openai import OpenAI
from dotenv import load_dotenv
from backend.models import Task
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_daily_summary():
    with Session() as session:
        tasks = session.query(Task).filter(Task.summary != "").all()
        if not tasks:
            print("No tasks with summaries found.")
            return

        descriptions = [f"{t.description} (Priority: {t.priority})" for t in tasks]
        task_text = "\n".join(descriptions)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate a concise daily summary of the following tasks, including key themes, priorities, and any recommendations."},
                {"role": "user", "content": f"Tasks:\n{task_text}"}
            ]
        )
        summary = response.choices[0].message.content
        print("Daily Task Summary:")
        print(summary)
        # In production, this could be emailed or stored

if __name__ == "__main__":
    generate_daily_summary()