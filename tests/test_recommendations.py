import sys
import os
from pathlib import Path

# Add both the root folder and app folder to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "app"))

try:
    from recommend import recommend_assessments  # Now works from both locations
except ImportError:
    try:
        from app.recommend import recommend_assessments
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\nFix this by:")
        print("1. Creating an empty __init__.py in your app folder")
        print("2. Running from the root folder (shl_recommender)")
        print("Current Python path:", sys.path)
        sys.exit(1)

def print_assessment(assessment, index):
    """Displays assessment details in a clean format"""
    print(f"\n{index}. {assessment['name']}")
    print(f"   📝 Description: {assessment.get('description', 'N/A')}")
    if 'skills' in assessment:
        print(f"   🔧 Skills: {', '.join(assessment['skills'])}")
    print(f"   ⏱️  Duration: {assessment['duration']}")
    print(f"   🌍 Remote: {assessment['remote_testing']}")
    print(f"   🎯 Adaptive: {assessment['adaptive']}")
    print(f"   🔗 URL: {assessment['url']}")

def run_tests():
    """Executes test cases against the recommendation engine"""
    test_cases = [
        "JavaScript coding test under 60 minutes",
        "Python algorithm assessment",
        "Full-stack developer test with React and Django",
        "Cognitive ability test for programmers",
        "Technical debugging challenge"
    ]

    print("\n" + "="*60)
    print("🔬 SHL RECOMMENDATION SYSTEM TESTING")
    print("="*60)

    for query in test_cases:
        print(f"\n🧪 TEST CASE: '{query}'")
        print("-"*50)
        
        try:
            results = recommend_assessments(query)
            if not results:
                print("⚠️  No matches found")
                continue
                
            for i, test in enumerate(results, 1):
                print_assessment(test, i)
                
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")

if __name__ == "__main__":
    print("📍 Working directory:", os.getcwd())
    print("📁 Project root:", Path(__file__).parent)
    run_tests()