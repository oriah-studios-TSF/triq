# triq

An AI-assisted IT support ticket analyzer built with Python and Flask.

triq analyses IT support ticket descriptions and generates structured results to help identify and understand reported technical issues.

## Features

- AI-powered ticket analysis using Qwen 3 1.7B.
- Automatic ticket categorisation.
- Priority assessment (Low, Medium, High).
- Automatic ticket summaries.
- Context-aware troubleshooting recommendations.
- Explanation of analysis results.
- Rule-based fallback when the AI service is unavailable.
- Input validation and error handling.

## Technologies

- Python
- Flask
- JavaScript
- HTML5
- CSS3
- Ollama
- Qwen 3 1.7B
- REST API
- Git

## How It Works

1. The user submits an IT support ticket.
2. Flask receives and validates the description.
3. The application sends the ticket to the locally running Qwen model through Ollama.
4. The model generates a structured analysis.
5. The response is validated before being returned.
6. If AI analysis fails, the application uses its rule-based analyzer.
7. The results are displayed in the frontend.

## Running Locally

### Requirements

- Python 3.10+
- Ollama

### Setup

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd triq
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` and configure:

```env
SECRET_KEY=your-secret-key
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:1.7b
```

Download the model:

```bash
ollama pull qwen3:1.7b
```

Start the application:

```bash
python run.py
```

Open `http://127.0.0.1:5000` in your browser.

## What I Worked On

This project gave me practical experience with:

- Building a backend application using Flask.
- Designing and implementing REST API endpoints.
- Integrating a locally hosted large language model.
- Working with structured AI-generated responses.
- Validating and handling external service responses.
- Implementing fallback logic for service failures.
- Connecting frontend JavaScript to backend API endpoints.
- Writing automated tests for application logic and API behaviour.

## Project Status

The core ticket analysis feature is implemented and working.

The project is part of my ongoing software development learning journey.
