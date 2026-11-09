# 🚀 HireAI - AI-Powered Recruitment & Portfolio Analysis Engine

HireAI is a high-performance AI microservice designed to automate the recruitment process. It analyzes job descriptions and candidate resumes/portfolios using a sophisticated **LangGraph-based pipeline**, providing real-time skill matching, document generation, and interview preparation.

## 🌟 Key Features

- **Dual PDF Parsing**: Support for uploading both Resumes and Job Descriptions as PDFs.
- **Intelligent Pipeline**: A multi-stage AI workflow powered by **LangGraph** for structured analysis.
- **Real-time Progress Tracking**: Integrated **Redis** state management to track pipeline progress (0% $\rightarrow$ 100%) in real-time.
- **LLM Integration**: Powered by **Ollama** for local, privacy-focused AI inference.
- **Asynchronous Execution**: Built with **FastAPI** and background tasks for non-blocking high-throughput processing.
- **Robust Infrastructure**: Fully containerized using **Docker** for seamless deployment.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | `FastAPI` | High-performance asynchronous API |
| **AI Orchestration** | `LangGraph` | Complex agentic workflows & state management |
| **LLM Engine** | `Ollama` | Local Large Language Model execution |
| **State Store** | `Redis` | Real-time job status and progress tracking |
| **Database** | `PostgreSQL` | Persistent storage for user profiles and jobs |
| **Parsing** | `PyMuPDF (fitz)` | High-accuracy PDF text extraction |
| **Infra** | `Docker` & `Docker Compose` | Containerization and orchestration |

---

## 🏗️ Architecture Flow

The system follows a sequential AI pipeline:
`JD Ingestion` $\rightarrow$ `Portfolio Analysis` $\rightarrow$ `Skill Matching` $\rightarrow$ `Doc Generation` $\rightarrow$ `QA Validation` $\rightarrow$ `Final Intel`

1. **Ingestion**: Extracts structured data from Job Descriptions (PDF/Text).
2. **Analysis**: Deep-dives into candidate portfolios.
3. **Matching**: Calculates semantic overlap between requirements and skills.
4. **Generation**: Creates tailored cover letters and cold emails.
5. **Validation**: A QA node ensures the output is accurate and professional.

---

## 🚀 Getting Started

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) & Docker Compose
- [Ollama](https://ollama.com/) (installed on host or running in container)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/hireai.git
   cd hireai
   ```

2. **Environment Configuration:**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@db:5432/hireai_db
   REDIS_URL=redis://redis:6379/0
   OLLAMA_BASE_URL=http://ollama:11434
   ```

3. **Launch the Services:**
   ```bash
   docker-compose up --build
   ```

---

## 📖 API Documentation

Once the server is running, you can access the interactive API documentation:

👉 **Swagger UI:** `http://localhost:8000/docs`

### Main Endpoints:
- `POST /v1/pipeline/run`: Start a new analysis (Supports PDF uploads for both Resume & JD).
- `GET /v1/pipeline/status/{job_id}`: Track real-time progress and fetch final results.
- `GET /health`: Check service availability.

---

## 🤝 Contributing
Contributions are welcome! Please fork the repository and create a pull request for any enhancements.

## 📜 License
This project is licensed under the MIT License.
