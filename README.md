# PictureSearch - Georgian Text Correction Module

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

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Google Cloud account with Gemini API access

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd picturesearch
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### 4. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API keys
nano .env
```

### 5. Configure API Keys

Edit the `.env` file and add your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 6. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Paste it in your `.env` file

### 7. Verify Installation

```bash
# Test the installation
python -c "import prompt_enhancer; print('Installation successful!')"
```

## Dependencies

### Core Dependencies

- **google-generativeai**: Google's Generative AI library for Gemini API
- **python-dotenv**: Environment variable management
- **requests**: HTTP library for API calls

### Development Dependencies

- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

## Environment Variables

| Variable         | Description           | Required | Example      |
| ---------------- | --------------------- | -------- | ------------ |
| `GOOGLE_API_KEY` | Google Gemini API key | Yes      | `AIzaSyC...` |

## File Structure

```
picturesearch/
├── prompt_enhancer/
│   ├── __init__.py
│   ├── georgian_corrector.py
│   ├── gemini_client.py
│   ├── cli.py
│   ├── api.py
│   └── tests/
│       ├── __init__.py
│       ├── run_tests.py
│       └── pipeline_tests/
│           ├── __init__.py
│           ├── test_examples.py
│           └── test_structure.py
├── requirements.txt
├── setup.py
├── .env.example
├── .env
└── README.md
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure virtual environment is activated
2. **API Key Error**: Verify your Google API key is correct and has Gemini access
3. **Permission Error**: Ensure you have write permissions in the project directory

### Getting Help

- Check the `.env` file configuration
- Verify your Google API key has Gemini API access
- Ensure all dependencies are installed correctly
- Check Python version compatibility

## License

This project is licensed under the MIT License - see the LICENSE file for details.
