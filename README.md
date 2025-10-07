# Lead Scoring API

This project is a backend service that accepts product information and a CSV of leads, then scores each lead's buying intent using a combination of rule-based logic and AI reasoning with the Google Gemini API.

## Live API

**Base URL:** https://kuvaka-lead-scorer.onrender.com/

## Features

-   **Offer Submission:** `POST /offer` endpoint to accept product/offer details.
-   **Lead Upload:** `POST /leads/upload` endpoint to process leads from a CSV file.
-   **Automated Scoring:** `POST /score` endpoint to trigger a hybrid scoring pipeline.
-   **Hybrid Scoring Logic:**
    -   **Rule-Based Layer (Max 50 pts):** Scores leads based on role, industry, and data completeness.
    -   **AI Layer (Max 50 pts):** Uses the Gemini API to analyze prospect data against the offer to determine buying intent (`High`, `Medium`, `Low`) and provide a reasoning statement.
-   **Retrieve Results:** `GET /results` endpoint to fetch all scored leads.

---

## Logic Explanation

### Rule-Based Scoring (Max 50 Points)
-   **Role Relevance:** `+20` points for decision-maker roles (e.g., 'Head', 'VP', 'Manager'), `+10` for influencers (e.g., 'Senior', 'Lead').
-   **Industry Match:** `+20` points for an ideal industry match (e.g., 'SaaS', 'Software'), `+10` for an adjacent industry (e.g., 'Tech', 'IT').
-   **Data Completeness:** `+10` points if all lead information fields are present.

### AI Prompt
The following prompt is sent to the Gemini API to provide context for its analysis:
```
You are an expert B2B sales development representative. Given the product offer and prospect information, classify the prospect's buying intent as High, Medium, or Low. Then, provide a concise, one-sentence explanation for your classification.

**Product Offer:**
- Name: {offer.name}
- Value Propositions: {', '.join(offer.value_props)}
- Ideal Use Cases: {', '.join(offer.ideal_use_cases)}

**Prospect Information:**
- Role: {lead.role} at {lead.company}
- Industry: {lead.industry}
- LinkedIn Bio: {lead.linkedin_bio}

Return your response ONLY in a valid JSON format with the keys "intent" and "reasoning".
```

---

## Setup and Installation

### 1. Local Setup

**Prerequisites:**
-   Python 3.13+
-   Poetry
-   A running PostgreSQL instance

**Steps:**
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/SatyamDev803/kuvaka-lead-scorer.git](https://github.com/SatyamDev803/kuvaka-lead-scorer.git)
    cd kuvaka-lead-scorer
    ```
2.  **Create a `.env` file** for local development with `localhost` for the database:
    ```
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
    GEMINI_API_KEY=your_google_ai_api_key
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
1.  **Create a `.env.docker` file** for the container with `host.docker.internal` for the database:
    ```
    DATABASE_URL=postgresql+asyncpg://user:password@host.docker.internal:5432/dbname
    GEMINI_API_KEY=your_google_ai_api_key
    ```
2.  **Build the Docker image:**
    ```bash
    docker build -t kuvaka-app .
    ```

---

## Running the Application

### Local
```bash
poetry run uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`, with interactive documentation at `http://127.0.0.1:8000/docs`.

### Docker
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


