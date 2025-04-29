from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import os
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Jetson Embedding API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://apps.medicpro.london"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model paths
MODEL_PATHS = {
    "all-MiniLM-L6-v2": "/home/mx/jetson-containers/data/models/torch/sentence_transformers/sentence-transformers_all-MiniLM-L6-v2",
    "all-mpnet-base-v2": "/home/mx/jetson-containers/data/models/torch/sentence_transformers/sentence-transformers_all-mpnet-base-v2"
}

# Load models
models = {}
for model_name, model_path in MODEL_PATHS.items():
    try:
        models[model_name] = SentenceTransformer(model_path)
        logger.info(f"Successfully loaded model: {model_name}")
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {str(e)}")

class TextInput(BaseModel):
    text: str
    model: str

@app.get("/models")
async def get_models():
    """Return available models"""
    return {"models": list(MODEL_PATHS.keys())}

@app.post("/embed")
async def generate_embedding(input_data: TextInput):
    """Generate embedding for input text using specified model"""
    if input_data.model not in models:
        raise HTTPException(status_code=400, detail=f"Model {input_data.model} not available")
    
    try:
        embedding = models[input_data.model].encode(input_data.text)
        return {"embedding": embedding.tolist()}
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating embedding")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 