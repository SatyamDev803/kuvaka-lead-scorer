# Lead Scoring API

This project is a backend service that accepts product information and a CSV of leads, then scores each lead's buying intent using a combination of rule-based logic and AI reasoning with the Google Gemini API.

## Features

-   **Offer Submission:** `POST /offer` endpoint to accept product/offer details.
-   **Lead Upload:** `POST /leads/upload` endpoint to process leads from a CSV file.
-   **Automated Scoring:** `POST /score` endpoint to trigger a hybrid scoring pipeline.
-   **Hybrid Scoring Logic:**
    -   **Rule-Based Layer (Max 50 pts):** Scores leads based on role, industry, and data completeness.
    -   **AI Layer (Max 50 pts):** Uses the Gemini API to analyze prospect data against the offer to determine buying intent (`High`, `Medium`, `Low`) and provide a reasoning statement.
-   **Retrieve Results:** `GET /results` endpoint to fetch all scored leads.
-   **Fully Dockerized:** Includes a `Dockerfile` for easy containerization.
-   **Tested:** Unit tests for the core rule-based scoring logic.

---

## Setup and Installation

### 1. Local Setup (with Poetry)

**Prerequisites:**
-   Python 3.11+
-   Poetry
-   A running PostgreSQL instance

**Steps:**
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SatyamDev803/kuvaka-lead-scorer.git
    cd kuvaka-assignment
    ```
2.  **Create a `.env` file** in the root directory and add your environment variables:
    ```
    DATABASE_URL="postgresql+asyncpg://user:password@host:port/dbname"
    GEMINI_API_KEY="your_google_ai_api_key"
    ```
3.  **Install dependencies:**
    ```bash
    poetry install
    ```
4.  **Run database migrations:**
    ```bash
    poetry run alembic upgrade head
    ```

### 2. Docker Setup

**Prerequisites:**
-   Docker Desktop

**Steps:**

1. Create a `.env.docker` file for the container. This file must use host.docker.internal for the database connection.
```
DATABASE_URL=postgresql+asyncpg://user:password@host.docker.internal:5432/dbname
GEMINI_API_KEY=your_google_ai_api_key
```
2. Build the Docker image:

```bash

docker build -t kuvaka-app .
```

---

## Running the Application

**Local**

Use the following command to run the server locally.
```bash
poetry run uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`, with interactive documentation at `http://1227.0.0.1:8000/docs`.

**Docker**

Use this command to run the application inside a container. It will load configuration from the .env.docker file.
```bash
docker run -p 8000:8000 --env-file .env.docker kuvaka-app
```
The API will be available at `http://127.0.0.1:8000`.

---

## API Usage (cURL Examples)

**1. Create an Offer:**
```bash
curl -X POST "[http://127.0.0.1:8000/offer](http://127.0.0.1:8000/offer)" -H "Content-Type: application/json" -d '{
  "name": "AI Outreach Automation",
  "value_props": ["24/7 outreach", "6x more meetings"],
  "ideal_use_cases": ["B2B SaaS mid-market"]
}'
```

**2. Upload Leads CSV:**
*(Requires a `leads.csv` file in the same directory)*
```bash
curl -X POST "[http://127.0.0.1:8000/leads/upload](http://127.0.0.1:8000/leads/upload)" -H "Content-Type: multipart/form-data" -F "file=@leads.csv"
```

**3. Trigger Scoring:**
```bash
curl -X POST "[http://127.0.0.1:8000/score](http://127.0.0.1:8000/score)"
```

**4. Get Results:**
```bash
curl -X GET "[http://127.0.0.1:8000/results](http://127.0.0.1:8000/results)"
```

---

## Live API

**Base URL:** `[Your Deployed URL Will Go Here]`