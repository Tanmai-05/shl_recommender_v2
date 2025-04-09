from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommend import recommend_assessments

# Define FastAPI app
app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoint
@app.get("/status")
def health():
    return {"status": "healthy"}

# Define the Request Body Model for the recommendation
class QueryRequest(BaseModel):
    query: str

# Define the response model for recommended assessments
class RecommendedAssessment(BaseModel):
    url: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: list

# Define the response model for the overall recommendations
class RecommendationsResponse(BaseModel):
    recommended_assessments: list[RecommendedAssessment]

# Main recommendation endpoint (POST request)
@app.post("/recommend", response_model=RecommendationsResponse)
async def get_recommendations(query: QueryRequest):
    try:
        # Get the recommendations based on the query
        results = recommend_assessments(query.query)

        if not results:
            raise HTTPException(status_code=404, detail="No recommendations found.")

        # Ensure to return a max of 10 recommendations
        recommendations = [
            RecommendedAssessment(
                url=a.get("url", ""),
                adaptive_support=a.get("adaptive_support", "No"),
                description=a.get("description", ""),
                duration=a.get("duration", 0),
                remote_support=a.get("remote_support", "No"),
                test_type=a.get("test_type", [])
            )
            for a in results[:10]  # Limit to 10 recommendations
        ]

        return RecommendationsResponse(recommended_assessments=recommendations)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
