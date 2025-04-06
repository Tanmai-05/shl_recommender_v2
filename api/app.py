from fastapi import FastAPI
from .recommend import recommend_assessments  # Your existing function

app = FastAPI()

@app.get("/recommend")
async def recommend(q: str):
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
                "type": test.get("type", "Technical")  # Add missing field
            }
            for test in results
        ]
    }