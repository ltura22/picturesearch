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
            "corrected": self._get_corrected_style_prompt(),
            "llm_friendly": self._get_llm_friendly_prompt(),
            "translate_to_english": self._get_translate_to_english_prompt(),
            "simplify": self._get_simplify_prompt(),
            "photo_agent": self._get_photo_agent_prompt()
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
        3. Do NOT change possessive forms that are already correct (like "ჩემი მეგობარი" should stay as "ჩემი მეგობარი")
        4. Do not change the meaning or context
        5. Do not add explanations or additional text
        6. Do NOT change word order unless there are actual grammatical errors
        7. Do NOT replace words with different meanings (like "წასვლა" should not become "წასვლის შემდეგ")
        8. Return ONLY the corrected sentence, nothing more
        
        Examples:
        - "დრეს ვმონაწილეობდი" -> "დღეს ვმონაწილეობდი" (fix typo)
        - "ვისაუბირეთ" -> "ვისაუბრეთ" (fix typo)
        - "ჩემი მეგობარი თბილისში წავიდა" -> "ჩემი მეგობარი თბილისში წავიდა" (no changes needed)
        - "დეს მე მივედი სკოლაში" -> "დღეს მე მივედი სკოლაში" (fix typo, keep word order)
        - "დრეს წასვლა და საღამო ერთად გავატარეთ" -> "დღეს წავედით და საღამო ერთად გავატარეთ" (fix typo and verb form)
        
        Text to correct: {text}
        
        Corrected sentence:
        """
    
    def _get_llm_friendly_prompt(self) -> str:
        """LLM-friendly correction prompt - makes text more clear for language models"""
        return """
        You are a Georgian language expert. Make the following Georgian text more LLM-friendly by adding clarity and explicit references ONLY when necessary.
        
        Rules:
        1. Add explicit subject pronouns (მე, შენ, ის, ჩვენ, etc.) ONLY when they are missing and needed for clarity
        2. Do NOT add pronouns if the sentence is already clear and grammatically correct
        3. Do NOT change existing subjects or possessive forms (like "ჩემი მეგობარი" should stay as "ჩემი მეგობარი")
        4. Fix any typos or spelling errors
        5. Keep the original meaning and context exactly the same
        6. Do NOT change the sentence structure unless there are actual errors
        7. For third person singular subjects, use "ის" (not "მათ")
        8. Do NOT change word order unless there are actual grammatical errors
        9. Return ONLY the LLM-friendly sentence, nothing more
        
        Examples:
        - "დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი, როცა მან დამარტყა და მცემა" 
          -> "მე დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი, როცა მან დამარტყა და მცემა"
        - "მოდი საქმე არ გავაკეთოთ" -> "მოდი, ჩვენ ეს საქმე არ გავაკეთოთ"
        - "ვაშლი ვჭამე" -> "მე ვაშლი ვჭამე"
        - "საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბრეთ." -> "საღამო კარგი იყო, ჩვენ მეგობრებთან ერთად ვისაუბრეთ."
        - "ჩემი მეგობარი თბილისში წავიდა და ახალი სამსახური დაიწყო." -> "ჩემი მეგობარი თბილისში წავიდა და ახალი სამსახური დაიწყო." (no changes needed)
        - "სკოლაში წავიდა და მეგობრებთან ერთად იმღერა." -> "ის სკოლაში წავიდა და მეგობრებთან ერთად იმღერა."
        - "დღეს წავედით და საღამო ერთად გავატარეთ." -> "ჩვენ დღეს წავედით და საღამო ერთად გავატარეთ."
        Text to make LLM-friendly: {text}
        
        LLM-friendly sentence:
        """
    
    def _get_translate_to_english_prompt(self) -> str:
        """Translate to English prompt"""
        return """
        You are a professional Georgian to English translator. Translate the following Georgian text to English.
        
        Rules:
        1. Provide accurate and natural English translation
        2. Maintain the original meaning and context
        3. Use appropriate English grammar and style
        4. Preserve the tone (formal/casual) of the original text
        5. Translate idiomatic expressions appropriately
        6. Return ONLY the English translation, nothing more
        
        Examples:
        - "გამარჯობა, როგორ ხარ?" -> "Hello, how are you?"
        - "დღეს ძალიან კარგი ამინდია" -> "The weather is very good today"
        - "მე სკოლაში ვსწავლობ" -> "I study at school"
        - "ჩვენ მეგობრებთან ერთად ვისაუბრეთ" -> "We talked with friends"
        
        Georgian text to translate: {text}
        
        English translation:
        """
    
    def _get_simplify_prompt(self) -> str:
        """Simplify prompt - extracts essential search terms from user prompts"""
        return """
        You are a Georgian language expert. Extract only the essential object/search terms from the following Georgian text by removing unnecessary action words and commands.
        
        Rules:
        1. Remove action words like "მიპოვე" (find me), "გამოიჩინე" (show), "მომწოდე" (give me), etc.
        2. Remove location/source phrases like "ამ ფოტოებიდან" (from these photos), "ამ სურათებიდან" (from these images), etc.
        3. Remove auxiliary phrases like "გთხოვთ" (please), "შეიძლება" (can you), etc.
        4. Convert descriptive phrases to simple object names when possible:
           - "ცხენის ფოტო" -> "ცხენი"
           - "ძაღლის სურათი" -> "ძაღლი"
           - "მანქანის ფოტო" -> "მანქანა"
        5. Keep descriptive adjectives and relative clauses that describe the object:
           - "რომელზეც კაცი ზის" (on which a man sits)
           - "რომელიც წითელია" (which is red)
        6. Return ONLY the essential object description, nothing more
        
        Examples:
        - "ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელზეც კაცი ზის" -> "ცხენი რომელზეც კაცი ზის"
        - "გთხოვთ გამოიჩინოთ ძაღლის სურათი რომელიც წითელია" -> "ძაღლი რომელიც წითელია"
        - "მიპოვე მანქანის ფოტო რომელიც ლურჯია" -> "მანქანა რომელიც ლურჯია"
        - "ამ სურათებიდან აირჩიე კატის ფოტო რომელიც იატაკზე წევს" -> "კატა რომელიც იატაკზე წევს"
        - "გამოიჩინე ადამიანის ფოტო რომელსაც წითელი კაბა აცვია" -> "ადამიანი რომელსაც წითელი კაბა აცვია"
        
        Text to simplify: {text}
        
        Essential object description:
        """
    
    def _get_photo_agent_prompt(self) -> str:
        """Prompt for photo agent to analyze prompts and extract photo search information"""
        return """
        You are a Georgian photo search agent. Analyze the following Georgian prompt and extract the number of photos requested and whether it's a photo search query.
        
        Rules:
        1. Detect if this is a photo search request. It MUST contain:
           - Photo/image words: "ფოტო", "სურათი", "ფოტოები", "სურათები"
           - AND action words: "მიპოვე", "გამოიჩინე", "მომწოდე", "აირჩიე", "მოძებნე", "ნახე"
           - OR location phrases: "ამ ფოტოებიდან", "ამ სურათებიდან", "საქაღალდეში", "კოლექციაში"
        
        2. Extract the number of photos requested:
           - "ფოტო" (singular without number) = 1
           - "ფოტოები" (plural without specific number) = 5 (default plural)
           - Numbers with "ფოტო": "ერთი ფოტო"=1, "ორი ფოტო"=2, "სამი ფოტო"=3, etc.
           - Digits with "ფოტო": "1 ფოტო"=1, "11 ფოტო"=11, "9 ფოტო"=9, etc.
           - "ცალი" means "pieces": "11 ცალი ფოტო"=11, "5 ცალი ფოტო"=5
        
        3. Return in format: "count|is_photo_search"
           - count: exact number (1, 3, 5, 9, 11, etc.) or "1" if not specified
           - is_photo_search: "yes" or "no"
        
        4. NOT photo search if:
           - Only contains object names without photo keywords: "ცხვარი", "მზე", "კატა"
           - Only contains "ფოტო" but no action words: "მზის ფოტო"
           - Negative statements without action: "ფოტო არ მაქვს"
        
        Examples:
        - "ჩემს საქაღალდეში მიპოვე ფოტო რომელშიც ნათლად ჩანს კაცი და ქალი" → "1|yes"
        - "ჩემს საქაღალდეში მიპოვე ფოტოები რომელშიც ნათლად ჩანს კაცი და ქალი" → "5|yes"
        - "ჩემს საქაღალდეში მიპოვე სამი ფოტო რომელშიც ნათლად ჩანს კაცი და ქალი" → "3|yes"
        - "ჩემს საქაღალდეში მიპოვე 9 ფოტო რომელშიც ნათლად ჩანს კაცი და ქალი" → "9|yes"
        - "მზის 11 ცალი ფოტო მიპოვე" → "11|yes"
        - "ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელზეც კაცი ზის" → "1|yes"
        - "მზის ფოტო" → "1|no" (no action word)
        - "ცხვარი" → "1|no" (no photo keywords)
        - "გამარჯობა, როგორ ხარ?" → "1|no"
        - "მზის 11 ცალი ფოტო" → "11|no" (no action word)
        - "ფოტო არ მაქვს" → "1|no" (negative, no action)
        
        Georgian numbers to recognize:
        - ერთი=1, ორი=2, სამი=3, ოთხი=4, ხუთი=5, ექვსი=6, შვიდი=7, რვა=8, ცხრა=9, ათი=10
        - Also recognize digits: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, etc.
        
        Prompt to analyze: {text}
        
        Result:
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
        
        # Note: Removed automatic typo correction since double letters and other patterns
        # are often correct in Georgian and should be handled by the LLM
        
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

    def translate_to_english(self, text: str) -> str:
        """
        Translate Georgian text to English
        
        Args:
            text: Georgian text to translate
            
        Returns:
            English translation
        """
        if not text or not text.strip():
            return text
        
        # Preprocess the text
        processed_text = self._preprocess_text(text)
        
        # Get translation prompt
        prompt_template = self.correction_prompts["translate_to_english"]
        prompt = prompt_template.format(text=processed_text)
        
        # Get translation from Gemini
        try:
            translated_text = ask_gemini(prompt)
            return translated_text.strip()
        except Exception as e:
            print(f"Error during translation: {e}")
            return processed_text
    
    def batch_translate_to_english(self, texts: List[str]) -> List[str]:
        """
        Translate multiple Georgian texts to English
        
        Args:
            texts: List of Georgian texts to translate
            
        Returns:
            List of English translations
        """
        translated_texts = []
        for text in texts:
            translated = self.translate_to_english(text)
            translated_texts.append(translated)
        return translated_texts

    def simplify_text(self, text: str) -> str:
        """
        Simplify Georgian text by extracting only essential search terms
        
        Args:
            text: Georgian text to simplify (usually a command or search query)
            
        Returns:
            Simplified text with only essential object descriptions
        """
        if not text or not text.strip():
            return text
        
        # Preprocess the text
        processed_text = self._preprocess_text(text)
        
        # Get simplification prompt
        prompt_template = self.correction_prompts["simplify"]
        prompt = prompt_template.format(text=processed_text)
        
        # Get simplified text from Gemini
        try:
            simplified_text = ask_gemini(prompt)
            return simplified_text.strip()
        except Exception as e:
            print(f"Error during simplification: {e}")
            return processed_text
    
    def batch_simplify(self, texts: List[str]) -> List[str]:
        """
        Simplify multiple Georgian texts
        
        Args:
            texts: List of Georgian texts to simplify
            
        Returns:
            List of simplified texts
        """
        simplified_texts = []
        for text in texts:
            simplified = self.simplify_text(text)
            simplified_texts.append(simplified)
        return simplified_texts

    def pipeline_correct(self, text: str, show_steps: bool = True, include_translation: bool = False) -> Dict[str, str]:
        """
        Pipeline correction: input -> corrected -> llm_friendly -> (optional) translation -> output
        
        Args:
            text: Input Georgian text
            show_steps: Whether to print intermediate results
            include_translation: Whether to include English translation in the pipeline
            
        Returns:
            Dictionary with all pipeline steps and final result
        """
        if not text or not text.strip():
            return {"error": "No text provided"}
        
        results = {
            "input": text,
            "corrected": "",
            "llm_friendly": "",
            "final": ""
        }
        
        if include_translation:
            results["translation"] = ""
        
        if show_steps:
            pipeline_steps = "Input -> Corrected -> LLM-Friendly"
            if include_translation:
                pipeline_steps += " -> Translation"
            pipeline_steps += " -> Output"
            print(f"Pipeline: {pipeline_steps}")
            print("=" * 60)
            print(f"1. Input: {text}")
        
        # Step 1: Correct typos and sentence structure
        corrected_text = self.correct_text(text, style="corrected")
        results["corrected"] = corrected_text
        
        if show_steps:
            print(f"2. Corrected: {corrected_text}")
        
        # Step 2: Make LLM-friendly
        llm_friendly_text = self.correct_text(corrected_text, style="llm_friendly")
        results["llm_friendly"] = llm_friendly_text
        
        if show_steps:
            print(f"3. LLM-Friendly: {llm_friendly_text}")
        
        # Step 3: Translate to English (optional)
        if include_translation:
            translated_text = self.translate_to_english(llm_friendly_text)
            results["translation"] = translated_text
            results["final"] = translated_text
            
            if show_steps:
                print(f"4. Translation: {translated_text}")
        else:
            results["final"] = llm_friendly_text
        
        if show_steps:
            print("=" * 60)
            print(f"Final Result: {results['final']}")
        
        return results
    
    def batch_pipeline_correct(self, texts: List[str], show_steps: bool = True, include_translation: bool = False) -> List[Dict[str, str]]:
        """
        Batch pipeline correction for multiple texts
        
        Args:
            texts: List of Georgian texts
            show_steps: Whether to print intermediate results
            include_translation: Whether to include English translation in the pipeline
            
        Returns:
            List of dictionaries with pipeline results for each text
        """
        results = []
        
        for i, text in enumerate(texts, 1):
            if show_steps:
                print(f"\n--- Processing Text {i}/{len(texts)} ---")
            
            result = self.pipeline_correct(text, show_steps, include_translation)
            results.append(result)
            
            if show_steps and i < len(texts):
                print()  # Add spacing between texts
        
        return results

    def simplify_pipeline_correct(self, text: str, show_steps: bool = True) -> Dict[str, str]:
        """
        Simplify pipeline: input -> corrected -> simplified -> output
        Perfect for processing search queries to extract essential terms
        
        Args:
            text: Input Georgian text (usually a search query or command)
            show_steps: Whether to print intermediate results
            
        Returns:
            Dictionary with all pipeline steps and final simplified result
        """
        if not text or not text.strip():
            return {"error": "No text provided"}
        
        results = {
            "input": text,
            "corrected": "",
            "simplified": "",
            "final": ""
        }
        
        if show_steps:
            print("Simplify Pipeline: Input -> Corrected -> Simplified -> Output")
            print("=" * 60)
            print(f"1. Input: {text}")
        
        # Step 1: Correct typos and grammar
        corrected_text = self.correct_text(text, style="corrected")
        results["corrected"] = corrected_text
        
        if show_steps:
            print(f"2. Corrected: {corrected_text}")
        
        # Step 2: Simplify to extract essential terms
        simplified_text = self.simplify_text(corrected_text)
        results["simplified"] = simplified_text
        results["final"] = simplified_text
        
        if show_steps:
            print(f"3. Simplified: {simplified_text}")
            print("=" * 60)
            print(f"Final Result: {results['final']}")
        
        return results
    
    def batch_simplify_pipeline_correct(self, texts: List[str], show_steps: bool = True) -> List[Dict[str, str]]:
        """
        Batch simplify pipeline correction for multiple texts
        
        Args:
            texts: List of Georgian texts (usually search queries)
            show_steps: Whether to print intermediate results
            
        Returns:
            List of dictionaries with simplify pipeline results for each text
        """
        results = []
        
        for i, text in enumerate(texts, 1):
            if show_steps:
                print(f"\n--- Processing Query {i}/{len(texts)} ---")
            
            result = self.simplify_pipeline_correct(text, show_steps)
            results.append(result)
            
            if show_steps and i < len(texts):
                print()  # Add spacing between texts
        
        return results

class PhotoAgent:
    """
    Agentic structure for photo search queries
    Automatically determines when to use simplify pipeline and extracts photo count
    """
    
    def __init__(self):
        self.corrector = GeorgianTextCorrector()
    
    def analyze_prompt(self, text: str) -> Dict[str, any]:
        """
        Analyze Georgian prompt to determine if it's a photo search and extract information
        
        Args:
            text: Georgian prompt text
            
        Returns:
            Dictionary with analysis results
        """
        if not text or not text.strip():
            return {
                "is_photo_search": False,
                "photo_count": 0,
                "simplified_query": "",
                "analysis": "empty_prompt"
            }
        
        # Use the photo agent prompt to analyze
        prompt_template = self.corrector.correction_prompts["photo_agent"]
        prompt = prompt_template.format(text=text)
        
        try:
            # Get analysis from Gemini
            response = ask_gemini(prompt)
            response = response.strip()
            
            # Parse response format: "count|is_photo_search"
            if "|" in response:
                count_str, is_search = response.split("|", 1)
                count_str = count_str.strip()
                is_search = is_search.strip().lower()
                
                is_photo_search = is_search == "yes"
                
                # Parse count
                photo_count = 1  # default
                if count_str.isdigit():
                    photo_count = int(count_str)
                elif count_str == "unknown":
                    photo_count = 1
                else:
                    try:
                        photo_count = int(count_str)
                    except:
                        photo_count = 1
                
                return {
                    "is_photo_search": is_photo_search,
                    "photo_count": photo_count,
                    "analysis": "success",
                    "raw_response": response
                }
            else:
                return {
                    "is_photo_search": False,
                    "photo_count": 0,
                    "analysis": "parse_error",
                    "raw_response": response
                }
                
        except Exception as e:
            return {
                "is_photo_search": False,
                "photo_count": 0,
                "analysis": f"error: {str(e)}",
                "simplified_query": ""
            }
    
    def process_prompt(self, text: str, show_steps: bool = True) -> Dict[str, any]:
        """
        Process Georgian prompt with agentic structure
        Automatically applies simplify pipeline if it's a photo search
        
        Args:
            text: Georgian prompt text
            show_steps: Whether to show processing steps
            
        Returns:
            Dictionary with processing results
        """
        if show_steps:
            print("Photo Agent: Analyzing prompt...")
        
        # Step 1: Analyze the prompt
        analysis = self.analyze_prompt(text)
        
        if show_steps:
            print(f"Analysis: {analysis}")
        
        result = {
            "original": text,
            "is_photo_search": analysis["is_photo_search"],
            "photo_count": analysis["photo_count"],
            "analysis": analysis["analysis"]
        }
        
        # Step 2: If it's a photo search, apply simplify pipeline
        if analysis["is_photo_search"]:
            if show_steps:
                print("Detected photo search - applying simplify pipeline...")
            
            pipeline_result = self.corrector.simplify_pipeline_correct(text, show_steps=show_steps)
            result.update({
                "simplified_query": pipeline_result["final"],
                "pipeline_steps": pipeline_result,
                "processing_type": "simplify_pipeline"
            })
        else:
            if show_steps:
                print("Not a photo search - no pipeline applied")
            
            result.update({
                "simplified_query": text,
                "processing_type": "no_processing"
            })
        
        return result
    
    def batch_process_prompts(self, texts: List[str], show_steps: bool = True) -> List[Dict[str, any]]:
        """
        Process multiple prompts with agentic structure
        
        Args:
            texts: List of Georgian prompt texts
            show_steps: Whether to show processing steps
            
        Returns:
            List of processing results
        """
        results = []
        
        for i, text in enumerate(texts, 1):
            if show_steps:
                print(f"\n--- Processing Prompt {i}/{len(texts)} ---")
            
            result = self.process_prompt(text, show_steps)
            results.append(result)
            
            if show_steps and i < len(texts):
                print()  # Add spacing between prompts
        
        return results

# Convenience functions for easy use
def correct_georgian_text(text: str, style: str = "auto") -> str:
    """Simple function to correct Georgian text"""
    corrector = GeorgianTextCorrector()
    return corrector.correct_text(text, style)

def batch_correct_georgian(texts: List[str], style: str = "auto") -> List[str]:
    """Simple function to correct multiple Georgian texts"""
    corrector = GeorgianTextCorrector()
    return corrector.batch_correct(texts, style)

def translate_georgian_to_english(text: str) -> str:
    """Simple function to translate Georgian text to English"""
    corrector = GeorgianTextCorrector()
    return corrector.translate_to_english(text)

def batch_translate_georgian_to_english(texts: List[str]) -> List[str]:
    """Simple function to translate multiple Georgian texts to English"""
    corrector = GeorgianTextCorrector()
    return corrector.batch_translate_to_english(texts)

def simplify_georgian_text(text: str) -> str:
    """Simple function to simplify Georgian text"""
    corrector = GeorgianTextCorrector()
    return corrector.simplify_text(text)

def batch_simplify_georgian(texts: List[str]) -> List[str]:
    """Simple function to simplify multiple Georgian texts"""
    corrector = GeorgianTextCorrector()
    return corrector.batch_simplify(texts)

def pipeline_correct_georgian(text: str, show_steps: bool = True, include_translation: bool = False) -> Dict[str, str]:
    """Simple function to run pipeline correction on Georgian text"""
    corrector = GeorgianTextCorrector()
    return corrector.pipeline_correct(text, show_steps, include_translation)

def batch_pipeline_correct_georgian(texts: List[str], show_steps: bool = True, include_translation: bool = False) -> List[Dict[str, str]]:
    """Simple function to run batch pipeline correction on Georgian texts"""
    corrector = GeorgianTextCorrector()
    return corrector.batch_pipeline_correct(texts, show_steps, include_translation)

def simplify_pipeline_correct_georgian(text: str, show_steps: bool = True) -> Dict[str, str]:
    """Simple function to run simplify pipeline on Georgian text (corrected -> simplified)"""
    corrector = GeorgianTextCorrector()
    return corrector.simplify_pipeline_correct(text, show_steps)

def batch_simplify_pipeline_correct_georgian(texts: List[str], show_steps: bool = True) -> List[Dict[str, str]]:
    """Simple function to run batch simplify pipeline on Georgian texts"""
    corrector = GeorgianTextCorrector()
    return corrector.batch_simplify_pipeline_correct(texts, show_steps)

# Photo Agent convenience functions
def analyze_photo_prompt(text: str) -> Dict[str, any]:
    """Simple function to analyze a Georgian photo prompt"""
    agent = PhotoAgent()
    return agent.analyze_prompt(text)

def process_photo_prompt(text: str, show_steps: bool = True) -> Dict[str, any]:
    """Simple function to process a Georgian photo prompt with agentic structure"""
    agent = PhotoAgent()
    return agent.process_prompt(text, show_steps)

def batch_process_photo_prompts(texts: List[str], show_steps: bool = True) -> List[Dict[str, any]]:
    """Simple function to process multiple Georgian photo prompts"""
    agent = PhotoAgent()
    return agent.batch_process_prompts(texts, show_steps)

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