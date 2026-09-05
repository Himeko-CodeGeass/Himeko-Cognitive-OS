from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from core.gestalt_engine import GestaltEngine

app = FastAPI(title="Himeko Cognitive OS - Gateway", version="1.0.0")

# 初始化格式塔意圖引擎
gestalt_engine = GestaltEngine(capacity=5)

class IntentRequest(BaseModel):
    input_text: str
    context: Optional[Dict[str, Any]] = None

@app.post("/api/v1/intent/process")
async def process_intent(request: IntentRequest):
    try:
        context_data = request.context if request.context is not None else {}
        result = gestalt_engine.process_intent(request.input_text, context_data)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "engine": "GestaltEngine active"}
