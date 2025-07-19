"""
Standalone Gemini Client for prompt_enhancer module
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def ask_gemini(prompt, model="gemini-1.5-flash"):
    """
    Simple function to send a prompt to Gemini and get a response
    Uses gemini-1.5-flash by default (best free model)
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        return "Error: GOOGLE_API_KEY not found in .env file"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "No response generated"
            
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Simple example usage
    prompt = input("Enter your prompt: ")
    response = ask_gemini(prompt)
    print("\nGemini Response:")
    print(response) 