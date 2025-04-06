from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .recommend import recommend_assessments

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health check endpoint (required to prevent 404)
@app.get("/")
def health_check():
    return {
        "status": "API is running",
        "endpoints": {
            "docs": "/docs",
            "recommendations": "/recommend?q=QUERY"
        }
    }

# Main recommendation endpoint
@app.get("/recommend")
async def recommend(q: str):
    try:
        results = recommend_assessments(q)
        return {
            "query": q,
            "results": [
                {
                    "name": test["name"],
                    "url": test["url"],
                    "remote_testing": test["remote_testing"],
                    "adaptive": test["adaptive"],
                    "duration": test["duration"],
                    "type": test.get("type", "Technical")
                }
                for test in results
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "solution": "Check if recommend_assessments() is properly defined in recommend.py"
        }
