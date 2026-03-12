# Sentinel: Google Cloud Life Sciences Agentic Platform

Sentinel has been transformed into a comprehensive, multi-workflow agentic platform for Life Sciences research, drug discovery, and regulatory compliance. Optimized for **Google Cloud**, it leverages the **Agent Development Kit (ADK)** and **Gemini 3** to orchestrate complex scientific tasks.

**Core Scientific Workflows:**

*   **Protein Folding & Simulation:** Specialized workflow using **AlphaFold on Vertex AI** for high-accuracy protein structure prediction and molecular dynamics.
*   **Pathway Analysis & Network Modeling:** Bioinformatics workflow for gene enrichment analysis and biological knowledge graph queries powered by **BigQuery**.
*   **Pharmaceutical Regulatory Review (Sentinel Core):** Advanced compliance checking for pharma advertisements and promotional materials (FDA/EMA standards).
*   **Biomedical Literature Discovery:** Expert agents for deep-dive research across **PubMed** and unstructured data via **Vertex AI Search**.

**Key Features:**

*   **Multi-Agent Orchestration:** A central `LifeSciencesPlatform` coordinator that intelligently routes requests to domain-specific workflows.
*   **GCP Native Tools:** Direct integration with Vertex AI (AlphaFold, Gemini), BigQuery, and Discovery Engine.
*   **Streaming Agentic Chat:** Real-time, asynchronous interaction with agents via a specialized FastAPI backend.
*   **Extensible Architecture:** Easily add new scientific workflows or expert agents as research needs evolve.

**Technology Stack:**

*   **Backend:** FastAPI, Google ADK, GenAI SDK.
*   **AI Models:** Gemini 3 Powerful (Pro) on Vertex AI.
*   **Infrastructure:** Cloud Run, Vertex AI Endpoints, GCS, BigQuery.
*   **Frontend:** React with Material Design.

**Life Science Tools Integrated:**

*   **PubMed Tool:** Real-time search and abstract retrieval from NCBI.
*   **ChEMBL Tool:** Molecular property and bioactivity data lookup.
*   **Vertex AI Search Tool:** Optimized grounding and search over large medical datasets.
*   **Regulatory Review Tool:** Specialized prompts for FDA/EMA compliance checking.

**Important Note:**

Sentinel code is a content analysis starter code and is for administrative and operational support only. It is not intended for any medical purpose, including diagnosis, prevention, monitoring, treatment, or alleviation of disease, injury, or disability, nor for the investigation, replacement, or modification of anatomy or physiological processes, or for the control of conception. Its function is solely to assist regulatory and marketing teams in identifying potential issues in pharmaceutical content. All outputs from Sentinel code should be considered preliminary, require independent verification and further investigation through established company process and methodologies for determining regulatory compliance for marketing content. This code is not intended to be used without appropriate validation, adaptation and/or making meaningful modifications by developers for their specific workflows. This code is intended as a developer accelerator and proof-of-concept. It has not undergone software validation (CSV), penetration testing, or quality assurance required for production environments in regulated industries. Deploying this code into a production workflow without significant modification, security hardening, and appropriate validation is at the user's sole risk.

> [!IMPORTANT]
> **A Note for Developers and Administrators:**
> By default, Vertex AI may collect data to improve service quality. Data collection and logging are **only disabled** if the user explicitly disables **Vertex AI data caching** within the Google Cloud project settings. 

For technical details on how to configure these settings, please refer to the official [Vertex AI Zero Data Retention Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/vertex-ai-zero-data-retention).


## Local Development

### Prerequisites

- Python 3.12+
- `uv` package manager (**required** - faster than pip/venv)
- Node.js and npm (for frontend)
- Google Cloud Project (for Vertex AI - preferred) OR Google Gemini API key (for AI Studio)
- Google Cloud SDK (for Vertex AI authentication)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GoogleCloudPlatform/LifeSciences
   cd LifeSciences
   ```

2. **Environment Configuration**:
   
   Copy `.env.example` to `.env` and fill in the required values.
   
   ```bash
   cp .env.example .env
   ```

   **Required for Agents:**
   *   `GCP_USER_ACCOUNT`: Your Google account email (required for `adkweb`).
   *   `GOOGLE_CLOUD_PROJECT`: Your GCP Project ID.

3. **Backend & Tooling Setup**:
   
   Run the configuration script to set up the nested `uv` environment (`.venv/python312`) and install dependencies:

   ```bash
   source .scripts/configure.sh
   ```

4. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

5. **Run the Development Servers**:

   * **Backend**:
      ```bash
      uv run python -m api.main
      ```
      The API will run at `http://localhost:8000`.

   * **ADK Web UI** (for Agent testing):
      ```bash
      adkweb
      ```
      The Agent UI will be available at `http://localhost:8001`.

   * **Frontend**:
      ```bash
      cd frontend
      npm run dev
      ```
      The frontend will run at `http://localhost:5173`.

### Running Tests

The project uses `pytest` for unit testing the API services and routes.

```bash
uv run pytest
```

## Docker Deployment

The application is containerized using a multi-stage Docker build that serves the React frontend via the FastAPI backend.

### Build and Run

1. **Build the Image**:
   ```bash
   docker build -t sentinel .
   ```

2. **Run the Container**:

   * **Run with AI Studio (API Key)**

      ```bash
      docker run -p 8080:8080 --env-file .env sentinel
      ```

   * **Run with Vertex AI**

      You need to provide your Google Cloud credentials to the container.

      ```bash
      # Authenticate locally first
      gcloud auth application-default login

      # Run container with mounted credentials and environment file
      # We use --user to ensure the container can read the mounted credentials
      docker run -p 8080:8080 \
      --user $(id -u):$(id -g) \
      -v ~/.config/gcloud/application_default_credentials.json:/app/gcp_creds.json \
      -e GOOGLE_APPLICATION_CREDENTIALS=/app/gcp_creds.json \
      --env-file .env \
      sentinel
      ```


## Project Structure

```
sentinel/
├── api/                    # FastAPI backend
│   ├── agents/            # ADK Agents (Coordinator, Literature, DB, Compliance)
│   ├── routes/            # API route handlers (analysis, agents, storage, health)
│   ├── services/          # Business logic (Agent service, Gemini client, analyzer)
│   ├── tools/             # Specialized tools (PubMed, ChEMBL, Vertex Search)
│   ├── models/            # Pydantic schemas
│   ├── config.py          # Configuration management
│   └── main.py            # FastAPI application entry point
├── tests/                  # Unit test suite
├── frontend/              # React frontend
├── Dockerfile              # Multi-stage Docker build
├── pyproject.toml         # Python dependencies and metadata
└── README.md               # This file
```

## API Endpoints

- `POST /agents/chat` - Interact with the agentic coordinator (Streaming)
- `POST /api/v1/analyze` - Analyze video (URL) or image (URL)
- `POST /api/v1/analyze/upload` - Analyze uploaded image file
- `GET /api/v1/storage/list` - List files in GCS
- `POST /api/v1/storage/upload` - Upload file to GCS
- `GET /health` - Health check

## Usage

### Analyze a YouTube Video

1. Select "YouTube Video" from the content type dropdown
2. Paste the YouTube URL
3. Optionally adjust the frame rate (lower = fewer tokens used)
4. Click "Analyze"

### Analyze an Image

1. Select "Image URL" or "Upload Image"
2. Provide the image URL or select a file
3. Click "Analyze"
4. Click on numbered markers to see issue details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


