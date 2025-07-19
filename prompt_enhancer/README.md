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

# File processing
python -m prompt_enhancer --file input.txt --output corrected.txt --style advanced

# Batch processing with JSON output
python -m prompt_enhancer --file texts.txt --batch --json --stats

# Show help
python -m prompt_enhancer --help
```

### Simple Function Usage

```python
from prompt_enhancer.georgian_corrector import correct_georgian_text

# Correct a single text
text = "გამარჯობა როგორ ხარ დღეს ძაან კარგი ამინდია"
corrected = correct_georgian_text(text, style="auto")
print(corrected)
```

### Class-based Usage

```python
from prompt_enhancer.georgian_corrector import GeorgianTextCorrector

corrector = GeorgianTextCorrector()

# Correct with specific style
corrected = corrector.correct_text("თქვენი ტექსტი", style="formal")

# Batch correction
texts = ["ტექსტი 1", "ტექსტი 2", "ტექსტი 3"]
corrected_texts = corrector.batch_correct(texts, style="casual")

# Get statistics
stats = corrector.get_correction_stats(original_text, corrected_text)
```

### API Usage

```python
from prompt_enhancer.api import correct_text_api, correct_batch_api

# Single text correction
result = correct_text_api("თქვენი ტექსტი", style="advanced")
print(result['corrected'])

# Batch correction
results = correct_batch_api(["ტექსტი 1", "ტექსტი 2"], style="formal")
for result in results['results']:
    print(result['corrected'])
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

## Pipeline Feature

The pipeline feature processes text through two stages sequentially:

1. **Corrected Stage**: Fixes typos and sentence structure
2. **LLM-Friendly Stage**: Makes text more explicit for language models

```bash
# Pipeline example
python -m prompt_enhancer "დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი" --pipeline

# Output shows each step:
# 1. Input: დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი
# 2. Corrected: დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი
# 3. LLM-Friendly: მე დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი
# Final Result: მე დღეს ძალიან მნიშვნელოვან ადამიანს ვესაუბრებოდი
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
2. Update the `correction_prompts` dictionary
3. Add tests for new functionality
4. Update documentation

## License

This module is part of the picturesearch project and follows the same license terms.
