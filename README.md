# AI Task Manager

[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat&logo=render)](https://your-frontend-url.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full-stack AI-powered task management application built with FastAPI, React, PostgreSQL, and OpenAI embeddings. Deployed on Render's free tier, it leverages semantic search via pgvector for intelligent task organization.

![Demo GIF](assets/demo.gif)

## 🚀 Features

- **AI-Powered Summarization & Prioritization**: Automatically summarizes and prioritizes tasks using OpenAI GPT-4o-mini.
- **Semantic Search**: Natural language queries to find tasks via vector embeddings and cosine similarity.
- **Responsive UI**: Mobile-first React interface with Tailwind CSS.
- **Free Tier Deployment**: Zero-cost hosting on Render with managed PostgreSQL.
- **Markdown Rendering**: Rich task summaries displayed with proper formatting.

## 🛠 Tech Stack

- **Backend**: FastAPI (Python), SQLAlchemy, pgvector
- **Frontend**: React (TypeScript), Vite, Tailwind CSS, Axios
- **Database**: PostgreSQL with pgvector extension
- **AI**: OpenAI API (embeddings & chat completions)
- **Deployment**: Render (Web Service, Static Site, Managed DB)
- **Local Dev**: Docker Compose

## 📋 Prerequisites

- Node.js (v18+)
- Python 3.10+
- Git
- OpenAI API Key (free tier available)
- Render Account (free)

## 🏗 Installation & Setup

### Local Development

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-username/ai-task-pipeline.git
   cd ai-task-pipeline

2. **Backend Setup:**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt

3. **Frontend Setup:**:
   ```bash
   cd frontend
   npm install
   cd ..

4. **Database:**:
   ```bash
   docker-compose up -d  # Starts PostgreSQL with pgvector

5. **Environment Variables:**:
    Create .env in root:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_task_db

6. **Run Locally:**:
   ```bash
   # Backend (in one terminal)
   python backend/main.py

   # Frontend (in another)
   cd frontend && npm run dev
    
* Backend: http://localhost:8000
* Frontend: http://localhost:5173

### Production Deployment

1. **Push to GitHub** (connect your repo to Render).

2. **Deploy via Render Blueprint**:
   - Use `render.yaml` for IaC.
   - Set `OPENAI_API_KEY` in Render dashboard.
   - Enable pgvector: `psql -h your-db-host -U your-user -d your-db -c "CREATE EXTENSION IF NOT EXISTS vector;"`

3. **URLs**:
   - Frontend: https://your-frontend-url.onrender.com
   - API: https://your-api.onrender.com

## 📖 Usage

1. **Add Tasks**: Enter a description; AI generates summary and priority.
2. **Search**: Use natural language (e.g., "high priority AI tasks").
3. **View Results**: See formatted summaries with priority badges.

### API Endpoints

- `POST /tasks`: Create a task
- `POST /query`: Search tasks

## 🤝 Contributing

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m 'feat: add your feature'`.
4. Push: `git push origin feature/your-feature`.
5. Open a PR.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by modern AI workflows and Render's developer tools.
- Built for demo purposes; extend with auth, async processing, etc.

