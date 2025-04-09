from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .recommend import recommend_assessments

# Define the FastAPI app
app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health check endpoint (required to prevent 404)
@app.get("/status")
def health_check():
    return {"status": "healthy"}

# Define the Request Body Model for the recommendation
class RecommendationRequest(BaseModel):
    query: str

# Define the response model for recommendations
class RecommendedAssessment(BaseModel):
    url: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: list

# Main recommendation endpoint (POST request)
@app.post("/recommend", response_model=dict)
async def recommend(request: RecommendationRequest):
    try:
        # Get the recommendations based on the query
        results = recommend_assessments(request.query)

        # Ensure to return a max of 10 recommendations
        recommendations = [
            RecommendedAssessment(
                url=test["url"],
                adaptive_support=test["adaptive"],
                description=test.get("description", "No description available"),
                duration=test["duration"],
                remote_support=test["remote_testing"],
                test_type=test.get("type", ["Technical"])
            )
            for test in results[:10]  # Limit to 10 recommendations
        ]

        return {"recommended_assessments": recommendations}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

