"""
API Interface for Georgian Text Correction
"""

from .georgian_corrector import GeorgianTextCorrector, pipeline_correct_georgian, batch_pipeline_correct_georgian, simplify_pipeline_correct_georgian, batch_simplify_pipeline_correct_georgian, process_photo_prompt, batch_process_photo_prompts

class GeorgianCorrectionAPI:
    """API interface for Georgian text correction"""
    
    def __init__(self):
        self.corrector = GeorgianTextCorrector()
    
    def correct_single(self, text: str, style: str = "auto") -> dict:
        """Correct a single text"""
        try:
            corrected = self.corrector.correct_text(text, style)
            stats = self.corrector.get_correction_stats(text, corrected)
            
            return {
                "success": True,
                "original": text,
                "corrected": corrected,
                "style": style,
                "stats": stats
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original": text
            }
    
    def correct_batch(self, texts: list, style: str = "auto") -> dict:
        """Correct multiple texts"""
        try:
            corrected_texts = self.corrector.batch_correct(texts, style)
            results = []
            
            for i, (original, corrected) in enumerate(zip(texts, corrected_texts)):
                stats = self.corrector.get_correction_stats(original, corrected)
                results.append({
                    "original": original,
                    "corrected": corrected,
                    "style": style,
                    "stats": stats
                })
            
            return {
                "success": True,
                "results": results,
                "total_texts": len(texts)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "total_texts": len(texts)
            }
    
    def translate_single(self, text: str) -> dict:
        """Translate a single text to English"""
        try:
            translated = self.corrector.translate_to_english(text)
            
            return {
                "success": True,
                "original": text,
                "translated": translated
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original": text
            }
    
    def translate_batch(self, texts: list) -> dict:
        """Translate multiple texts to English"""
        try:
            translated_texts = self.corrector.batch_translate_to_english(texts)
            results = []
            
            for original, translated in zip(texts, translated_texts):
                results.append({
                    "original": original,
                    "translated": translated
                })
            
            return {
                "success": True,
                "results": results,
                "total_texts": len(texts)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "total_texts": len(texts)
            }
    
    def simplify_single(self, text: str) -> dict:
        """Simplify a single text to extract essential search terms"""
        try:
            simplified = self.corrector.simplify_text(text)
            
            return {
                "success": True,
                "original": text,
                "simplified": simplified
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original": text
            }
    
    def simplify_batch(self, texts: list) -> dict:
        """Simplify multiple texts to extract essential search terms"""
        try:
            simplified_texts = self.corrector.batch_simplify(texts)
            results = []
            
            for original, simplified in zip(texts, simplified_texts):
                results.append({
                    "original": original,
                    "simplified": simplified
                })
            
            return {
                "success": True,
                "results": results,
                "total_texts": len(texts)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "total_texts": len(texts)
            }
    
    def pipeline_single(self, text: str, include_translation: bool = False) -> dict:
        """Run pipeline on a single text"""
        try:
            result = pipeline_correct_georgian(text, show_steps=False, include_translation=include_translation)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original": text
            }
    
    def pipeline_batch(self, texts: list, include_translation: bool = False) -> dict:
        """Run pipeline on multiple texts"""
        try:
            results = batch_pipeline_correct_georgian(texts, show_steps=False, include_translation=include_translation)
            return {
                "success": True,
                "results": results,
                "total_texts": len(texts)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "total_texts": len(texts)
            }
    
    def simplify_pipeline_single(self, text: str) -> dict:
        """Run simplify pipeline on a single text (corrected -> simplified)"""
        try:
            result = simplify_pipeline_correct_georgian(text, show_steps=False)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original": text
            }
    
    def simplify_pipeline_batch(self, texts: list) -> dict:
        """Run simplify pipeline on multiple texts"""
        try:
            results = batch_simplify_pipeline_correct_georgian(texts, show_steps=False)
            return {
                "success": True,
                "results": results,
                "total_texts": len(texts)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "total_texts": len(texts)
            }
    
    def agent_single(self, text: str) -> dict:
        """Process a single text with photo agent (auto-detects photo search)"""
        try:
            result = process_photo_prompt(text, show_steps=False)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original": text
            }
    
    def agent_batch(self, texts: list) -> dict:
        """Process multiple texts with photo agent"""
        try:
            results = batch_process_photo_prompts(texts, show_steps=False)
            return {
                "success": True,
                "results": results,
                "total_texts": len(texts)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "total_texts": len(texts)
            }
    
    def get_available_styles(self) -> list:
        """Get list of available correction styles"""
        return list(self.corrector.correction_prompts.keys())

# Convenience functions for direct API access
def correct_text_api(text: str, style: str = "auto") -> dict:
    """API function to correct text"""
    api = GeorgianCorrectionAPI()
    return api.correct_single(text, style)

def correct_batch_api(texts: list, style: str = "auto") -> dict:
    """API function to correct multiple texts"""
    api = GeorgianCorrectionAPI()
    return api.correct_batch(texts, style)

def translate_text_api(text: str) -> dict:
    """API function to translate text to English"""
    api = GeorgianCorrectionAPI()
    return api.translate_single(text)

def translate_batch_api(texts: list) -> dict:
    """API function to translate multiple texts to English"""
    api = GeorgianCorrectionAPI()
    return api.translate_batch(texts)

def pipeline_text_api(text: str, include_translation: bool = False) -> dict:
    """API function to run pipeline on text"""
    api = GeorgianCorrectionAPI()
    return api.pipeline_single(text, include_translation)

def pipeline_batch_api(texts: list, include_translation: bool = False) -> dict:
    """API function to run pipeline on multiple texts"""
    api = GeorgianCorrectionAPI()
    return api.pipeline_batch(texts, include_translation)

def simplify_text_api(text: str) -> dict:
    """API function to simplify text to extract essential search terms"""
    api = GeorgianCorrectionAPI()
    return api.simplify_single(text)

def simplify_batch_api(texts: list) -> dict:
    """API function to simplify multiple texts to extract essential search terms"""
    api = GeorgianCorrectionAPI()
    return api.simplify_batch(texts)

def simplify_pipeline_text_api(text: str) -> dict:
    """API function to run simplify pipeline on text (corrected -> simplified)"""
    api = GeorgianCorrectionAPI()
    return api.simplify_pipeline_single(text)

def simplify_pipeline_batch_api(texts: list) -> dict:
    """API function to run simplify pipeline on multiple texts"""
    api = GeorgianCorrectionAPI()
    return api.simplify_pipeline_batch(texts)

def agent_text_api(text: str) -> dict:
    """API function to process text with photo agent (auto-detects photo search)"""
    api = GeorgianCorrectionAPI()
    return api.agent_single(text)

def agent_batch_api(texts: list) -> dict:
    """API function to process multiple texts with photo agent"""
    api = GeorgianCorrectionAPI()
    return api.agent_batch(texts) 