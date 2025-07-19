"""
Simple API interface for Georgian Text Correction
"""

from .georgian_corrector import GeorgianTextCorrector, correct_georgian_text, batch_correct_georgian
import json
from typing import Dict, List, Any

class GeorgianCorrectionAPI:
    """
    Simple API interface for Georgian text correction
    """
    
    def __init__(self):
        self.corrector = GeorgianTextCorrector()
    
    def correct_single(self, text: str, style: str = "auto") -> Dict[str, Any]:
        """
        Correct a single text
        
        Args:
            text: Georgian text to correct
            style: Correction style
            
        Returns:
            Dictionary with original, corrected text and stats
        """
        if not text:
            return {"error": "No text provided"}
        
        original = text
        corrected = self.corrector.correct_text(text, style)
        stats = self.corrector.get_correction_stats(original, corrected)
        
        return {
            "original": original,
            "corrected": corrected,
            "style": style,
            "stats": stats,
            "success": True
        }
    
    def correct_batch(self, texts: List[str], style: str = "auto") -> Dict[str, Any]:
        """
        Correct multiple texts
        
        Args:
            texts: List of Georgian texts
            style: Correction style
            
        Returns:
            Dictionary with results
        """
        if not texts:
            return {"error": "No texts provided"}
        
        results = []
        for text in texts:
            result = self.correct_single(text, style)
            results.append(result)
        
        return {
            "results": results,
            "total_texts": len(texts),
            "style": style,
            "success": True
        }
    
    def get_available_styles(self) -> List[str]:
        """Get available correction styles"""
        return list(self.corrector.correction_prompts.keys()) + ["auto"]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get module statistics"""
        return {
            "available_styles": self.get_available_styles(),
            "common_typos": len(self.corrector.common_georgian_typos),
            "module_version": "1.0.0"
        }

# Global API instance
api = GeorgianCorrectionAPI()

# Convenience functions
def correct_text_api(text: str, style: str = "auto") -> Dict[str, Any]:
    """Simple API function to correct text"""
    return api.correct_single(text, style)

def correct_batch_api(texts: List[str], style: str = "auto") -> Dict[str, Any]:
    """Simple API function to correct multiple texts"""
    return api.correct_batch(texts, style)

if __name__ == "__main__":
    # Example API usage
    print("Georgian Correction API")
    print("=" * 30)
    
    # Test single correction
    test_text = "გამარჯობა როგორ ხარ დღეს ძაან კარგი ამინდია"
    result = correct_text_api(test_text, "auto")
    print(f"Single correction result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # Test batch correction
    test_texts = [
        "გთხოვთ მომაწოდოთ ინფორმაცია",
        "მე ვარ სტუდენტი და ვსწავლობ"
    ]
    batch_result = correct_batch_api(test_texts, "formal")
    print(f"\nBatch correction result: {json.dumps(batch_result, indent=2, ensure_ascii=False)}")
    
    # Get available styles
    styles = api.get_available_styles()
    print(f"\nAvailable styles: {styles}") 