import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommend import recommend_assessments
import threading
import socket

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

# Define the response model for individual recommended assessments
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
async def recommend(request: RecommendationRequest):
    try:
        # Get the recommendations based on the query
        results = recommend_assessments(request.query)

        if not results:
            raise HTTPException(status_code=404, detail="No recommendations found.")

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

        return RecommendationsResponse(recommended_assessments=recommendations)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Function to check if the port is available
def is_port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', port))
        return result != 0

# Function to find an available port
def find_available_port(start_port: int = 8502, max_retries: int = 10) -> int:
    port = start_port
    for _ in range(max_retries):
        if is_port_available(port):
            return port
        port += 1
    raise Exception("No available port found.")

# Function to run the Streamlit app in a separate process
def run_streamlit():
    port = find_available_port()  # Find the first available port
    try:
        subprocess.run(["streamlit", "run", "api/streamlit_app.py", "--server.port", str(port)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit app: {e}")

# Start the Streamlit app in a separate thread
streamlit_thread = threading.Thread(target=run_streamlit)
streamlit_thread.start()

