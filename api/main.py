from fastapi import FastAPI
from pydantic import BaseModel
from recommend import recommend_assessments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional: CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}

# Recommendation Request Body
class QueryRequest(BaseModel):
    query: str

# Recommend Endpoint
@app.post("/recommend")
def get_recommendations(query: QueryRequest):
    assessments = recommend_assessments(query.query, max_results=10)
    return {
        "recommended_assessments": [
            {
                "url": a.get("url", ""),
                "adaptive_support": a.get("adaptive_support", "No"),
                "description": a.get("description", ""),
                "duration": a.get("duration", 0),
                "remote_support": a.get("remote_support", "No"),
                "test_type": a.get("test_type", [])
            }
            for a in assessments
        ]
    }
