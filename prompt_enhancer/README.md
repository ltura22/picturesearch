# Georgian Text Correction Module

A microservice-style prompt engineering module for correcting bad Georgian text with typos using Google's Gemini AI.

## Features

- **Multiple Correction Styles**: Basic, advanced, contextual, formal, and casual
- **Auto-detection**: Automatically detects text context and applies appropriate corrections
- **Batch Processing**: Correct multiple texts at once
- **Statistics**: Get detailed correction statistics
- **API Interface**: Simple API for integration
- **CLI Tool**: Command-line interface for easy testing
- **Preprocessing**: Handles common Georgian typing errors
- **Translation**: Translate Georgian text to English
- **Pipeline Processing**: Multi-stage correction with optional translation

## Installation

1. Make sure you have the virtual environment activated:

```bash
source venv/bin/activate
```

2. Install the package in development mode:

```bash
pip install -e .
```

3. Set up your Google API key in `.env` file:

```
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

### Command Line Interface (Recommended)

```bash
# Interactive mode
python -m prompt_enhancer --interactive

# Single text correction
python -m prompt_enhancer "გამარჯობა როგორ ხარ" --style formal

# Pipeline correction (corrected -> llm_friendly)
python -m prompt_enhancer "დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი" --pipeline

# Pipeline with translation (corrected -> llm_friendly -> english)
python -m prompt_enhancer "საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბირეთ." --pipeline --translate

# Extract essential search terms (simplify)
python -m prompt_enhancer "ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელზეც კაცი ზის" --style simplify

# Simplify pipeline (corrected -> simplified)
python -m prompt_enhancer "ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელეც კაც ზის" --simplify-pipeline

# Direct translation to English
python -m prompt_enhancer "გამარჯობა, როგორ ხარ?" --style translate_to_english

# File processing
python -m prompt_enhancer --file input.txt --output corrected.txt --style advanced

# Batch processing with JSON output
python -m prompt_enhancer --file texts.txt --batch --json --stats

# Show help
python -m prompt_enhancer --help
```

### Simple Function Usage

```python
from prompt_enhancer.georgian_corrector import correct_georgian_text, translate_georgian_to_english, simplify_georgian_text

# Correct a single text
text = "გამარჯობა როგორ ხარ დღეს ძაან კარგი ამინდია"
corrected = correct_georgian_text(text, style="auto")
print(corrected)

# Translate to English
english = translate_georgian_to_english(text)
print(english)

# Simplify text to extract essential search terms
search_query = "ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელზეც კაცი ზის"
simplified = simplify_georgian_text(search_query)
print(simplified)  # Output: "ცხენი რომელზეც კაცი ზის"
```

### Class-based Usage

```python
from prompt_enhancer.georgian_corrector import GeorgianTextCorrector

corrector = GeorgianTextCorrector()

# Correct with specific style
corrected = corrector.correct_text("თქვენი ტექსტი", style="formal")

# Translate to English
english = corrector.translate_to_english("გამარჯობა, როგორ ხარ?")

# Batch correction
texts = ["ტექსტი 1", "ტექსტი 2", "ტექსტი 3"]
corrected_texts = corrector.batch_correct(texts, style="casual")

# Batch translation
english_texts = corrector.batch_translate_to_english(texts)

# Simplify text to extract essential search terms
simplified = corrector.simplify_text("ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელზეც კაცი ზის")
print(simplified)  # Output: "ცხენი რომელზეც კაცი ზის"

# Batch simplification
search_queries = ["ამ ფოტოებიდან მიპოვე ძაღლის ფოტო", "გთხოვთ გამოიჩინოთ კატის სურათი"]
simplified_queries = corrector.batch_simplify(search_queries)

# Simplify pipeline (corrected -> simplified)
pipeline_result = corrector.simplify_pipeline_correct("ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელეც კაც ზის")
print(pipeline_result['final'])  # Output: "ცხენი რომელზეც კაცი ზის"

# Batch simplify pipeline
queries = ["ამ ფოტოებიდან მიპოვე ძაღლის ფოტო", "გთხოვთ გამოიჩინოთ კატის სურათი"]
pipeline_results = corrector.batch_simplify_pipeline_correct(queries)

# Get statistics
stats = corrector.get_correction_stats(original_text, corrected_text)
```

### API Usage

```python
from prompt_enhancer.api import correct_text_api, translate_text_api, pipeline_text_api, simplify_text_api

# Single text correction
result = correct_text_api("თქვენი ტექსტი", style="advanced")
print(result['corrected'])

# Single text translation
result = translate_text_api("გამარჯობა, როგორ ხარ?")
print(result['translated'])

# Single text simplification
result = simplify_text_api("ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელზეც კაცი ზის")
print(result['simplified'])  # Output: "ცხენი რომელზეც კაცი ზის"

# Simplify pipeline (corrected -> simplified)
result = simplify_pipeline_text_api("ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელეც კაც ზის")
print(result['result']['final'])  # Output: "ცხენი რომელზეც კაცი ზის"

# Pipeline with translation
result = pipeline_text_api("დღეს კარგი ამინდია", include_translation=True)
print(result['result']['final'])  # English translation
```

## Correction Styles

- **auto**: Automatically detects context and applies appropriate corrections
- **basic**: Simple spelling and grammar corrections
- **advanced**: Advanced corrections with context awareness
- **formal**: Formal/business language corrections
- **casual**: Casual/informal language corrections
- **contextual**: Context-aware corrections
- **corrected**: Only fixes typos and sentence structure (minimal changes)
- **llm_friendly**: Makes text more LLM-friendly by adding explicit subject pronouns and clarifying references
- **translate_to_english**: Translates Georgian text to English
- **simplify**: Extracts essential search terms by removing action words and commands

## Pipeline Feature

The pipeline feature processes text through multiple stages sequentially:

### Standard Pipeline

1. **Corrected Stage**: Fixes typos and sentence structure
2. **LLM-Friendly Stage**: Makes text more explicit for language models
3. **Translation Stage** (optional): Translates to English

### Simplify Pipeline

1. **Corrected Stage**: Fixes typos and sentence structure
2. **Simplified Stage**: Extracts essential search terms by removing action words

```bash
# Basic pipeline
python -m prompt_enhancer "დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი" --pipeline

# Pipeline with translation
python -m prompt_enhancer "საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბირეთ." --pipeline --translate

# Simplify pipeline (perfect for search queries)
python -m prompt_enhancer "ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელეც კაც ზის" --simplify-pipeline

# Output shows each step:
# 1. Input: საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბირეთ.
# 2. Corrected: საღამო კარგი იყო, მეგობრებთან ერთად ვისაუბრეთ.
# 3. LLM-Friendly: საღამო კარგი იყო, ჩვენ მეგობრებთან ერთად ვისაუბრეთ.
# 4. Translation: The evening was pleasant; we chatted with friends.
# Final Result: The evening was pleasant; we chatted with friends.
```

## Translation Examples

```bash
# Direct translation
python -m prompt_enhancer "გამარჯობა, როგორ ხარ?" --style translate_to_english
# Output: "Hello, how are you?"

# Pipeline with translation
python -m prompt_enhancer "მე სკოლაში ვსწავლობ" --pipeline --translate
# Output: "I study at school"
```

## API Response Format

```json
{
  "original": "თქვენი ტექსტი",
  "corrected": "თქვენი ტექსტი",
  "style": "auto",
  "stats": {
    "original_length": 15,
    "corrected_length": 15,
    "character_changes": 0,
    "words_changed": 0,
    "improvement_ratio": 1.0
  },
  "success": true
}
```

## Examples

### Basic Correction

```bash
python -m prompt_enhancer "გამარჯობა როგორ ხარ დღეს ძაან კარგი ამინდია"
# Output: "გამარჯობა! როგორ ხარ? დღეს რა მაგარია ამინდი!"
```

### Formal Correction

```bash
python -m prompt_enhancer "გთხოვთ მომაწოდოთ ინფორმაცია პროდუქტის შესახებ" --style formal
# Output: "გთხოვთ, მომაწოდოთ ინფორმაცია პროდუქტის შესახებ."
```

### Translation

```bash
python -m prompt_enhancer "დღეს ძალიან კარგი ამინდია" --style translate_to_english
# Output: "The weather is very good today"
```

### Simplification (Extract Essential Search Terms)

```bash
python -m prompt_enhancer "ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელზეც კაცი ზის" --style simplify
# Output: "ცხენი რომელზეც კაცი ზის"

python -m prompt_enhancer "გთხოვთ გამოიჩინოთ ძაღლის სურათი რომელიც წითელია" --style simplify
# Output: "ძაღლი რომელიც წითელია"

python -m prompt_enhancer "მიპოვე მანქანის ფოტო რომელიც ლურჯია" --style simplify
# Output: "მანქანა რომელიც ლურჯია"
```

### Interactive Mode

```bash
python -m prompt_enhancer --interactive
# Enter text and style interactively
```

## Error Handling

The module includes comprehensive error handling:

- API key validation
- Network error handling
- Invalid input validation
- Graceful fallbacks

## Performance

- Uses Google's Gemini 1.5 Flash model (best free model)
- Optimized prompt engineering for faster responses
- Batch processing for multiple texts
- Caching of common corrections

## Contributing

To add new correction styles or improve the module:

1. Add new prompt templates in `GeorgianTextCorrector._get_*_correction_prompt()`
