import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Biodiversity AI")


# Store conversation information
conversation_memory = {}


# Allow frontend to connect to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load biodiversity knowledge
knowledge_path = Path("knowledge/knowledge.json")

with open(knowledge_path, "r", encoding="utf-8") as file:
    knowledge_base = json.load(file)


# Environmental data received from the user
class EnvironmentalData(BaseModel):
    session_id: str = "default"
    use_memory: bool = False
    region: str = ""
    rainfall: str = ""
    soil_carbon: float | None = None
    soil_ph: float | None = None
    soil_moisture: str = ""
    land_use: str = ""
    temperature: float | None = None
    question: str = ""


# Home page
@app.get("/")
def home():
    return {
        "message": "Biodiversity AI is running!",
        "status": "success"
    }


# Analyze environmental conditions
@app.post("/analyze")
def analyze(data: EnvironmentalData):

    recommendations = []

    # Get information from the previous conversation
    previous_data = (
        conversation_memory.get(data.session_id, {})
        if data.use_memory
        else {}
    )

    # Use previous information when the new message does not provide it
    if not data.region:
        data.region = previous_data.get("region", "")

    if not data.rainfall:
        data.rainfall = previous_data.get("rainfall", "")

    if data.soil_carbon is None:
        data.soil_carbon = previous_data.get("soil_carbon")

    if data.soil_ph is None:
        data.soil_ph = previous_data.get("soil_ph")

    if not data.soil_moisture:
        data.soil_moisture = previous_data.get("soil_moisture", "")

    if not data.land_use:
        data.land_use = previous_data.get("land_use", "")

    if data.temperature is None:
        data.temperature = previous_data.get("temperature")

    # Check for missing environmental information
    missing_fields = []

    if not data.rainfall:
        missing_fields.append("rainfall pattern")

    if not data.land_use:
        missing_fields.append("land use")

    if data.soil_carbon is None:
        missing_fields.append("soil organic carbon")

    # Ask for clarification if important information is missing
    if missing_fields:
        return {
            "region": data.region,
            "clarification_needed": True,
            "message": "I need a little more information before making a biodiversity recommendation.",
            "missing_information": missing_fields,
            "recommendations": []
        }

    # Save the updated conversation information
    conversation_memory[data.session_id] = {
        "region": data.region,
        "rainfall": data.rainfall,
        "soil_carbon": data.soil_carbon,
        "soil_ph": data.soil_ph,
        "soil_moisture": data.soil_moisture,
        "land_use": data.land_use,
        "temperature": data.temperature,
        "question": data.question
    }

    # Multi-metric reasoning
    if (
        data.soil_carbon < 0.5
        and (
            "low" in data.rainfall.lower()
            or "drought" in data.rainfall.lower()
        )
        and (
            "monoculture" in data.land_use.lower()
            or "single crop" in data.land_use.lower()
        )
        and (
            not data.soil_moisture
            or "low" in data.soil_moisture.lower()
            or "dry" in data.soil_moisture.lower()
        )
    ):
        recommendations.append({
            "topic": "Combined soil, water and biodiversity stress",
            "recommendation": "Use diversified planting such as legume intercropping or suitable agroforestry, retain crop residues, and use soil-cover or mulching practices.",
            "scientific_reason": "Low soil organic carbon can indicate limited organic inputs, while low rainfall increases water stress. Monoculture also provides less plant and habitat diversity. Combining soil-cover practices with diversified planting can address soil condition, moisture retention and habitat diversity together.",
            "impacted_metric": "Soil organic carbon, soil moisture, habitat diversity and biodiversity",
            "time_horizon": "Medium to long term",
            "confidence": "High",
            "measurement": "Measure soil organic carbon and soil moisture periodically and track plant and habitat diversity against the baseline.",
            "source": "FAO - Soil Organic Cover and Conservation Agriculture",
            "source_url": "https://www.fao.org/conservation-agriculture/in-practice/soil-organic-cover/en/"
        })

    # Soil pH reasoning
    if data.soil_ph is not None:

        if data.soil_ph < 5.5:
            data.question += " acidic soil"

        elif data.soil_ph > 8.0:
            data.question += " alkaline soil"

    # Temperature reasoning
    if data.temperature is not None:

        if data.temperature >= 35:
            data.question += " high temperature"

    # Combine the user's environmental information
    user_text = (
        f"{data.rainfall} "
        f"{data.land_use} "
        f"{data.region} "
        f"{data.question}"
    ).lower()

    # Add stress conditions only when they actually exist

    # Low soil organic carbon
    if data.soil_carbon is not None and data.soil_carbon < 0.5:
        user_text += " low soil organic carbon"

    # Low soil moisture
    if data.soil_moisture:
        moisture_text = data.soil_moisture.lower()

        if "low" in moisture_text or "dry" in moisture_text:
            user_text += " low soil moisture"

    # Low rainfall
    if data.rainfall:
        rainfall_text = data.rainfall.lower()

        if "low" in rainfall_text or "drought" in rainfall_text:
            user_text += " low rainfall"

    # Search the knowledge base
    for item in knowledge_base:
        for keyword in item["keywords"]:

            if keyword.lower() in user_text:

                recommendations.append({
                    "topic": item["topic"],
                    "recommendation": item["recommendation"],
                    "scientific_reason": item["scientific_reason"],
                    "impacted_metric": item["metric"],
                    "time_horizon": item["time_horizon"],
                    "confidence": item["confidence"],
                    "measurement": item["measurement"],
                    "source": item["source"],
                    "source_url": item["source_url"]
                })

                break

    # Return final analysis
    return {
        "region": data.region,
        "recommendations": recommendations,
        "impacted_metrics": [
            "Soil organic carbon",
            "Soil moisture",
            "Habitat diversity",
            "Biodiversity"
        ],
        "time_horizon": "Medium term"
    }