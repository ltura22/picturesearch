"""
Georgian Text Correction Module
A microservice-style prompt engineering module for correcting bad Georgian text with typos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .gemini_client import ask_gemini
import re
from typing import Dict, List, Optional, Tuple

class GeorgianTextCorrector:
    """
    A prompt engineering module for correcting Georgian text with typos
    Uses advanced prompt engineering techniques for optimal results
    """
    
    def __init__(self):
        self.correction_prompts = {
            "basic": self._get_basic_correction_prompt(),
            "advanced": self._get_advanced_correction_prompt(),
            "contextual": self._get_contextual_correction_prompt(),
            "formal": self._get_formal_correction_prompt(),
            "casual": self._get_casual_correction_prompt(),
            "corrected": self._get_corrected_style_prompt()
        }
        
        self.common_georgian_typos = {
            "აა": "ა",
            "ოო": "ო",
            "ეე": "ე",
            "იი": "ი",
            "უი": "უ",
            "უა": "უ",
            "ოა": "ო",
            "ეა": "ე",
            "ია": "ი"
        }
    
    def _get_basic_correction_prompt(self) -> str:
        """Basic correction prompt for simple typos"""
        return """
        You are a Georgian language expert. Correct the following Georgian text by fixing typos, spelling errors, and grammar mistakes.
        
        Rules:
        1. Keep the original meaning and tone
        2. Fix spelling errors and typos
        3. Correct grammar where needed
        4. Maintain proper Georgian script
        5. Return only the corrected text, no explanations
        
        Text to correct: {text}
        
        Corrected text:
        """
    
    def _get_advanced_correction_prompt(self) -> str:
        """Advanced correction prompt with context awareness"""
        return """
        You are an expert Georgian linguist and text correction specialist. 
        
        Task: Correct the following Georgian text with advanced error detection and correction.
        
        Instructions:
        1. Identify and fix spelling errors, typos, and grammar mistakes
        2. Consider context and meaning preservation
        3. Apply proper Georgian language rules and conventions
        4. Handle common Georgian typing errors (like double letters, wrong vowels)
        5. Maintain the original style and formality level
        6. Return only the corrected text
        
        Common Georgian corrections to apply:
        - Fix double vowels (აა→ა, ოო→ო, etc.)
        - Correct common typing mistakes
        - Fix word boundaries and spacing
        - Apply proper case endings
        
        Input text: {text}
        
        Corrected output:
        """
    
    def _get_contextual_correction_prompt(self) -> str:
        """Context-aware correction prompt"""
        return """
        As a Georgian language expert, correct this text while considering context and meaning.
        
        Context: This appears to be {context_type} text.
        
        Correction guidelines:
        1. Fix spelling and grammar errors
        2. Maintain appropriate formality level
        3. Preserve the intended meaning
        4. Consider the context type (formal/casual/technical)
        5. Apply domain-specific corrections if needed
        
        Text: {text}
        
        Corrected version:
        """
    
    def _get_formal_correction_prompt(self) -> str:
        """Formal text correction prompt"""
        return """
        Correct this Georgian text for formal/business use.
        
        Requirements:
        1. Fix all spelling and grammar errors
        2. Use formal Georgian language conventions
        3. Ensure professional tone
        4. Apply proper punctuation and formatting
        5. Use standard Georgian vocabulary
        
        Text: {text}
        
        Formal corrected text:
        """
    
    def _get_casual_correction_prompt(self) -> str:
        """Casual text correction prompt"""
        return """
        Correct this Georgian text for casual/informal use.
        
        Requirements:
        1. Fix spelling and grammar errors
        2. Maintain casual, friendly tone
        3. Keep natural Georgian expressions
        4. Preserve colloquial language where appropriate
        5. Ensure readability and clarity
        
        Text: {text}
        
        Casual corrected text:
        """
    
    def _get_corrected_style_prompt(self) -> str:
        """Corrected style prompt - only fixes typos and sentence structure"""
        return """
        You are a Georgian language expert. Correct the following Georgian text by fixing typos and sentence structure.
        
        Rules:
        1. Only fix spelling errors and typos
        2. Fix basic sentence structure issues
        3. Do not change the meaning or context
        4. Do not add explanations or additional text
        5. Return ONLY the corrected sentence, nothing more
        
        Text to correct: {text}
        
        Corrected sentence:
        """
    
    def _detect_context_type(self, text: str) -> str:
        """Detect the context type of the text"""
        formal_indicators = ["გთხოვთ", "მადლობა", "წინადადება", "მოთხოვნა", "დოკუმენტი"]
        casual_indicators = ["გამარჯობა", "როგორ ხარ", "კარგი", "მაგარი", "ძაან"]
        
        text_lower = text.lower()
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in text_lower)
        casual_count = sum(1 for indicator in casual_indicators if indicator in text_lower)
        
        if formal_count > casual_count:
            return "formal"
        elif casual_count > formal_count:
            return "casual"
        else:
            return "neutral"
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for better correction"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common immediate typos
        for typo, correction in self.common_georgian_typos.items():
            text = text.replace(typo, correction)
        
        return text
    
    def correct_text(self, text: str, style: str = "auto", context: Optional[str] = None) -> str:
        """
        Correct Georgian text with specified style
        
        Args:
            text: Input Georgian text with typos
            style: Correction style ("basic", "advanced", "contextual", "formal", "casual", "auto")
            context: Optional context information
            
        Returns:
            Corrected Georgian text
        """
        if not text or not text.strip():
            return text
        
        # Preprocess the text
        processed_text = self._preprocess_text(text)
        
        # Auto-detect style if not specified
        if style == "auto":
            detected_context = self._detect_context_type(processed_text)
            style = detected_context
        
        # Get appropriate prompt
        if style in self.correction_prompts:
            prompt_template = self.correction_prompts[style]
        else:
            prompt_template = self.correction_prompts["advanced"]
        
        # Format the prompt
        if style == "contextual":
            context_type = context or self._detect_context_type(processed_text)
            prompt = prompt_template.format(text=processed_text, context_type=context_type)
        else:
            prompt = prompt_template.format(text=processed_text)
        
        # Get correction from Gemini
        try:
            corrected_text = ask_gemini(prompt)
            return corrected_text.strip()
        except Exception as e:
            print(f"Error during correction: {e}")
            return processed_text
    
    def batch_correct(self, texts: List[str], style: str = "auto") -> List[str]:
        """
        Correct multiple texts in batch
        
        Args:
            texts: List of Georgian texts to correct
            style: Correction style
            
        Returns:
            List of corrected texts
        """
        corrected_texts = []
        for text in texts:
            corrected = self.correct_text(text, style)
            corrected_texts.append(corrected)
        return corrected_texts
    
    def get_correction_stats(self, original: str, corrected: str) -> Dict:
        """
        Get statistics about the correction
        
        Args:
            original: Original text
            corrected: Corrected text
            
        Returns:
            Dictionary with correction statistics
        """
        stats = {
            "original_length": len(original),
            "corrected_length": len(corrected),
            "character_changes": sum(1 for a, b in zip(original, corrected) if a != b),
            "words_changed": len(set(original.split()) - set(corrected.split())),
            "improvement_ratio": len(corrected) / len(original) if len(original) > 0 else 1.0
        }
        return stats

# Convenience functions for easy use
def correct_georgian_text(text: str, style: str = "auto") -> str:
    """Simple function to correct Georgian text"""
    corrector = GeorgianTextCorrector()
    return corrector.correct_text(text, style)

def batch_correct_georgian(texts: List[str], style: str = "auto") -> List[str]:
    """Simple function to correct multiple Georgian texts"""
    corrector = GeorgianTextCorrector()
    return corrector.batch_correct(texts, style)

if __name__ == "__main__":
    # Example usage
    corrector = GeorgianTextCorrector()
    
    test_texts = [
        "გამარჯობა როგორ ხარ დღეს ძაან კარგი ამინდია",
        "გთხოვთ მომაწოდოთ ინფორმაცია პროდუქტის შესახებ",
        "მე ვარ სტუდენტი და ვსწავლობ პროგრამირებას"
    ]
    
    print("Georgian Text Correction Module")
    print("=" * 50)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. Original: {text}")
        corrected = corrector.correct_text(text, "auto")
        print(f"   Corrected: {corrected}")
        
        stats = corrector.get_correction_stats(text, corrected)
        print(f"   Changes: {stats['character_changes']} characters") 