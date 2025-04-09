import json
import google.generativeai as genai
from pathlib import Path
import sys
import re  # Import regex module for parsing duration

# Configure Gemini with your API key (Method 1)
genai.configure(api_key="AIzaSyDitT4ynqqynhUAJwagX-RRXJcQy5IFaN0")  # Your key here
model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Updated model name

def parse_duration(duration: str):
    """Extract numeric value from a string like '60 minutes' or '30 mins'."""
    match = re.search(r'(\d+)', duration)
    if match:
        return int(match.group(1))  # Return the numeric part
    return 0  # Default if no numeric value found

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
        # Generate response from model
        response = model.generate_content(prompt)
        print(f"Response from model: {response.text}")  # Debug: Print model's response
        
        # Split the response text into indices
        selected_indices = [
            int(i.strip())-1 
            for i in response.text.split(",") 
            if i.strip().isdigit() and 0 <= int(i.strip())-1 < len(assessments)
        ]
        
        print(f"Selected indices: {selected_indices}")  # Debug: Print selected indices

        # If selected indices are empty, it means no valid results were returned
        if not selected_indices:
            print(f"No valid recommendations found for the query: {query}")
        
        # Parse the duration field here to handle string durations like '60 minutes'
        for i in selected_indices:
            assessments[i]['duration'] = parse_duration(assessments[i].get('duration', '0'))
        
        # Return top recommendations (max_results)
        return [assessments[i] for i in selected_indices[:max_results]]
    
    except Exception as e:
        print(f"Recommendation error: {e}")
        return []

