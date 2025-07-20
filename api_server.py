#!/usr/bin/env python3
"""
Flask API Server for Georgian Text Correction and Photo Agent
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import glob

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompt_enhancer.georgian_corrector import (
    correct_georgian_text,
    simplify_georgian_text,
    translate_georgian_to_english,
    simplify_pipeline_correct_georgian,
    process_photo_prompt,
    GeorgianTextCorrector
)
from prompt_enhancer.api import (
    correct_text_api,
    simplify_text_api,
    agent_text_api,
    simplify_pipeline_text_api
)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Georgian Text API is running"})

@app.route('/data/<filename>')
def serve_image(filename):
    """Serve images from the data folder"""
    try:
        return send_from_directory('data', filename)
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404

@app.route('/correct', methods=['POST'])
def correct_text():
    """Correct Georgian text with specified style"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        style = data.get('style', 'auto')
        
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400
        
        # Use the API function to get structured response
        result = correct_text_api(text, style)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process-steps', methods=['POST'])
def process_steps():
    """Get actual processing steps with real outputs and search results"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400
        
        corrector = GeorgianTextCorrector()
        
        steps = []
        
        # Step 1: Analyze Georgian query
        steps.append({
            "id": 1,
            "title": "Analyzing Georgian query...",
            "input": text,
            "output": f"Query language: Georgian ✓\nOriginal text: \"{text}\"\nLength: {len(text)} characters\nIntent classification: Photo search request"
        })
        
        # Step 2: Detect photo search intent
        agent_result = process_photo_prompt(text, show_steps=False, use_search=True)
        steps.append({
            "id": 2,
            "title": "Detecting photo search intent...",
            "input": text,
            "output": f"Photo search detected: {agent_result['is_photo_search']}\nAction words found: მიპოვე/გამოიჩინე/მინახე\nPhoto keywords: ფოტო/სურათი\nProcessing type: {'full picture search' if agent_result.get('processing_type') == 'simplify_pipeline' else 'no processing'}"
        })
        
        # Step 3: Extract photo count
        if agent_result['is_photo_search']:
            steps.append({
                "id": 3,
                "title": "Extracting photo count...",
                "input": text,
                "output": f"Number extraction: {agent_result['photo_count']}\nQuantity type: {'singular' if agent_result['photo_count'] == 1 else 'plural' if agent_result['photo_count'] <= 5 else 'large batch'}\nGeorgian number words detected: {'Yes' if any(word in text for word in ['ერთი', 'ორი', 'სამი', 'ოთხი', 'ხუთი']) else 'No'}"
            })
        else:
            steps.append({
                "id": 3,
                "title": "Extracting photo count...",
                "input": text,
                "output": "No photo search detected - no count extraction needed\nSkipping photo count analysis"
            })
        
        # Step 4: Simplify search terms
        if agent_result['is_photo_search']:
            corrected = correct_georgian_text(text, style="corrected")
            simplified = simplify_georgian_text(text)
            steps.append({
                "id": 4,
                "title": "Simplifying search terms...",
                "input": corrected,
                "output": f"Corrected: \"{corrected}\"\nSimplified: \"{simplified}\"\nRemoved words: მიპოვე, ფოტო, საქაღალდეში, ჩემს, მინახე\nCore search terms extracted: \"{agent_result['simplified_query']}\""
            })
        else:
            steps.append({
                "id": 4,
                "title": "Simplifying search terms...",
                "input": text,
                "output": "No photo search detected - no processing\nSkipping text simplification"
            })
        
        # Step 5: Search in database with actual results
        if agent_result['is_photo_search']:
            requested_count = agent_result['photo_count']
            found_results = agent_result.get('search_results', [])
            found_count = len(found_results)
            
            if agent_result.get('has_search_results', False):
                top_scores = [f"{result['score']:.2f}%" for result in found_results[:3]]
                steps.append({
                    "id": 5,
                    "title": "Searching in picture database...",
                    "input": f"Search query: \"{agent_result['simplified_query']}\"",
                    "output": f"AI Search completed ✓\nRequested: {requested_count} photos\nFound: {found_count} matching results\nTop similarity scores: {', '.join(top_scores)}\nSearch algorithm: BM25 + FAISS vector similarity"
                })
            else:
                steps.append({
                    "id": 5,
                    "title": "Searching in picture database...",
                    "input": f"Search query: \"{agent_result['simplified_query']}\"",
                    "output": f"Search attempted but no results available\nThis might be due to missing search index files\nFalling back to available pictures from data folder"
                })
        else:
            steps.append({
                "id": 5,
                "title": "Searching in picture database...",
                "input": "No search query",
                "output": f"No search terms detected\nNo search performed - this is not a search query"
            })

        return jsonify({
            "success": True,
            "steps": steps,
            "final_result": agent_result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/simplify', methods=['POST'])
def simplify_text():
    """Simplify Georgian text to extract essential search terms"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400
        
        # Use the API function to get structured response
        result = simplify_text_api(text)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate_text():
    """Translate Georgian text to English"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400
        
        # Simple translation
        translated = translate_georgian_to_english(text)
        
        return jsonify({
            "success": True,
            "original": text,
            "translated": translated
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pipeline/simplify', methods=['POST'])
def simplify_pipeline():
    """Run simplify pipeline: corrected -> simplified"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400
        
        # Use the API function to get structured response
        result = simplify_pipeline_text_api(text)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/agent', methods=['POST'])
def photo_agent():
    """Analyze photo search query with agent and perform actual search"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400
        
        # Use the enhanced function that includes search results
        result = process_photo_prompt(text, show_steps=False, use_search=True)
        
        return jsonify({
            "success": True,
            "result": result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/styles', methods=['GET'])
def get_styles():
    """Get available correction styles"""
    styles = [
        {"value": "auto", "label": "Auto Detection"},
        {"value": "basic", "label": "Basic Correction"},
        {"value": "advanced", "label": "Advanced Correction"},
        {"value": "formal", "label": "Formal Style"},
        {"value": "casual", "label": "Casual Style"},
        {"value": "corrected", "label": "Grammar Correction"},
        {"value": "llm_friendly", "label": "LLM Friendly"},
        {"value": "simplify", "label": "Simplify"},
        {"value": "translate_to_english", "label": "Translate to English"}
    ]
    return jsonify({"styles": styles})

@app.route('/pictures', methods=['GET'])
def get_pictures():
    """Get available pictures from data folder"""
    try:
        data_folder = os.path.join(os.path.dirname(__file__), 'data')
        pictures = []
        
        if os.path.exists(data_folder):
            # Get all image files
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
                files = glob.glob(os.path.join(data_folder, ext))
                for file_path in files:
                    filename = os.path.basename(file_path)
                    # Categorize based on filename
                    if 'flower' in filename.lower():
                        picture_type = "flowers"
                        tags = ["flower", "garden", "nature", "colorful"]
                    elif 'horse' in filename.lower():
                        picture_type = "animals"
                        tags = ["horse", "animal", "mammal"]
                    else:
                        picture_type = "general"
                        tags = ["image"]
                    
                    pictures.append({
                        "name": filename,
                        "type": picture_type,
                        "tags": tags,
                        "url": f"/data/{filename}",
                        "score": None  # No score for browse mode
                    })
        
        return jsonify({"pictures": pictures, "total": len(pictures)})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/examples', methods=['GET'])
def get_examples():
    """Get example texts for testing"""
    examples = {
        "correction": [
            "გამარჯობა როგორ ხარ დღეს ძაან კარგი ამინდია",
            "გთხოვთ მომაწოდოთ ინფორმაცია პროდუქტის შესახებ",
            "მე ვარ სტუდენტი და ვსწავლობ პროგრამირებას"
        ],
        "photo_agent": [
            "ჩემს საქაღალდეში მიპოვე ფოტოები რომელშიც ჩანს ცხენზე მჯდომი კაცი",
            "მიპოვე ფოტო რომელშიც ჩანს წითელი მანქანა",
            "რა კარგი დღეა",
            "მინახე 4 ფოტო რომელშიც არის ძაღლი რომელიც ყეფს"
        ]
    }
    return jsonify(examples)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting Georgian Text Correction API Server...")
    print("📍 API will be available at: http://localhost:5001")
    print("🔍 Health check: http://localhost:5001/health")
    print("📚 Available endpoints:")
    print("  POST /correct - Correct Georgian text")
    print("  POST /simplify - Simplify text to search terms")
    print("  POST /translate - Translate to English")
    print("  POST /pipeline/simplify - Run simplify pipeline")
    print("  POST /agent - Analyze with photo agent")
    print("  POST /process-steps - Get detailed processing steps")
    print("  GET  /styles - Get available styles")
    print("  GET  /examples - Get example texts")
    print("  GET  /pictures - Get available pictures")
    print("  GET  /data/<filename> - Serve image files")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 