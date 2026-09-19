# Biodiversity AI

AI-powered biodiversity and environmental recommendation system built for the Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge.

## Project Overview

Biodiversity AI is a conversational environmental intelligence system that combines structured environmental inputs, conversation memory, multi-metric reasoning, and a curated scientific knowledge base to generate actionable, evidence-backed biodiversity recommendations.

## Key Features

- Structured environmental data input
- Soil health and biodiversity analysis
- Rainfall and soil moisture analysis
- Land-use and temperature analysis
- Multi-metric reasoning
- Clarification when essential information is missing
- Conversational memory
- Evidence-backed recommendations
- Scientific source references
- Impacted environmental metrics
- Measurement guidance
- Time horizon and confidence information
- Web-based user interface

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- HTML
- CSS
- JavaScript
- JSON Knowledge Base

## System Architecture

```text
User
  ↓
Frontend (HTML/CSS/JavaScript)
  ↓
FastAPI Backend
  ↓
Conversation Memory
  ↓
Multi-Metric Reasoning
  ↓
Scientific Knowledge Base
  ↓
Evidence-Backed Recommendations
  ↓
Frontend Results
Knowledge Base

The project uses a structured knowledge base containing environmental topics such as:

*Low soil organic carbon
*Low soil moisture
*Monoculture
*Low rainfall
*Biodiversity habitat
*Soil pH stress
*High temperature stress
*Pollution stress
*Deforestation and habitat loss

Each knowledge entry contains:

*Recommendation
*Scientific reasoning
*Impacted metric
*Time horizon
*Confidence
*Measurement method
*Scientific source
Multi-Metric Reasoning

The system can identify combined environmental stress when multiple conditions occur together.

For example:

*Low soil organic carbon
*Low rainfall
*Low soil moisture
*Monoculture

These conditions can trigger a recommendation involving diversified planting, suitable agroforestry, residue retention, and soil-cover or mulching practices.

The recommendation connects the intervention with soil organic carbon, soil moisture, habitat diversity, and biodiversity.
Conversational Memory

The application supports conversation memory using a session ID.

Users can select Continue previous conversation to reuse previously stored environmental information when some values are omitted from a follow-up request.

When memory is disabled, the system treats the request as a fresh analysis.
Clarification Handling

If essential information such as rainfall, land use, or soil organic carbon is missing, the system asks the user for the missing information instead of generating an unsupported recommendation.
API
POST /analyze

The API accepts structured environmental information including:

*Region
*Rainfall
*Soil organic carbon
*Soil pH
*Soil moisture
*Land use
*Temperature
*User question
The response provides recommendations along with scientific reasoning, impacted metrics, measurement guidance, time horizon, confidence, and source information.
*Project Structure
BIODIVERSITY_AI/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── frontend/
│   └── index.html
│
└── knowledge/
    └── knowledge.json
Local Setup
1. Install dependencies
pip install -r requirements.txt
2. Start the backend
python -m uvicorn app:app --reload
3. Open the frontend
frontend/index.html
in a web browser.
The backend runs at:
http://127.0.0.1:8000
Scientific Evidence

The recommendation system uses scientific sources such as FAO and IPCC material. Each recommendation displayed by the application includes source information and measurement guidance.

Future Improvements
*Embedding and vector database-based retrieval
*Research paper and environmental report ingestion
*Geospatial inputs and biodiversity maps
*Larger species and habitat datasets
*Automated recommendation quality evaluation
*Production deployment
*CI/CD pipeline
