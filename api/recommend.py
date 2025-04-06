import json
import google.generativeai as genai
from pathlib import Path
import sys

# Configure Gemini with your API key (Method 1)
genai.configure(api_key="AIzaSyDitT4ynqqynhUAJwagX-RRXJcQy5IFaN0")  # Your key here
model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Updated model name

def load_assessments():
    """Load assessments from JSON file with error handling"""
    try:
        data_path = Path(__file__).parent.parent / 'data' / 'shl_assessments.json'
        with open(data_path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading assessments: {e}")
        sys.exit(1)

def recommend_assessments(query, max_results=5):
    """Get recommendations with enhanced error handling"""
    assessments = load_assessments()
    
    # Build prompt with assessment details
    assessment_text = "\n".join([
        f"{idx+1}. {a['name']}: {a.get('description', '')} "
        f"(Skills: {', '.join(a.get('skills', ['General']))} | "
        f"Duration: {a['duration']} | Type: {a['test_type']})"
        for idx, a in enumerate(assessments)
    ])
    
    prompt = f"""
    Recommend {max_results} assessments from:
    {assessment_text}
    
    For: "{query}"
    
    Consider:
    1. Skill matches
    2. Duration
    3. Test type
    
    Return ONLY numbers (1-{len(assessments)}) in order of relevance.
    Example: "2,3,1"
    """
    
    try:
        response = model.generate_content(prompt)
        selected_indices = [
            int(i.strip())-1 
            for i in response.text.split(",") 
            if i.strip().isdigit() and 0 <= int(i.strip())-1 < len(assessments)
        ]
        return [assessments[i] for i in selected_indices[:max_results]]
    
    except Exception as e:
        print(f"Recommendation error: {e}")
        return []

# For quick testing
if __name__ == "__main__":
    print("Testing with 'JavaScript test':")
    print(recommend_assessments("JavaScript test"))