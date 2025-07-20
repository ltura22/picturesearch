# Photo Search Agent - Georgian AI

A full-stack AI-powered application for searching and analyzing pictures using natural language queries in Georgian.

## 🚀 Features

### Photo Search Agent

- **Intelligent Query Analysis**: Automatically detects photo search intentions
- **Photo Count Extraction**: Extracts requested number of photos from Georgian text
- **Query Simplification**: Converts complex queries to essential search terms
- **Agentic Structure**: Smart processing pipeline that adapts to query type
- **Real-time Search Process**: Visual feedback showing search steps
- **Picture Database**: Browse available pictures with tags and categories

### Georgian Language Processing

- **Natural Language Understanding**: Processes Georgian text with AI
- **Number Recognition**: Recognizes numbers in Georgian (ერთი, ორი, სამი, etc.) and digits
- **Complex Pattern Handling**: Understands "ცალი" (pieces), plural forms, and various query structures

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   Flask API     │    │  Python Modules │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│  (AI Processing)│
│   Port: 3000    │    │   Port: 5001    │    │   Gemini AI     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- Google Gemini API Key

### 1. Clone the Repository

```bash
git clone https://github.com/ltura22/picturesearch/pulse
cd picturesearch
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the root directory with your Google Gemini API key:

```bash
# Create .env file using nano editor
nano .env
```

Copy and paste this template, then replace with your actual API key:

```env
# Google Gemini AI API Key
# Get your API key from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

**Important:**

- Replace `your_google_gemini_api_key_here` with your actual Google Gemini API key
- Save and exit nano: Press `Ctrl+X`, then `Y`, then `Enter`
- Keep your API key secure and never commit it to version control

To get a Google Gemini API key:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key and paste it in your `.env` file

#### Setup Picture Database

Create a `data` folder and add your pictures:

```bash
mkdir data
# Add your image files (*.jpg, *.jpeg, *.png, *.gif) to the data folder
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## 🚀 Running the Application

### Start Backend API Server

```bash
# From the root directory
source venv/bin/activate
python api_server.py
```

The API will be available at: `http://localhost:5001`

### Start Frontend Development Server

```bash
# In a new terminal
cd frontend
npm start
```

The React app will be available at: `http://localhost:3000`

### Stopping the Application

To stop running processes:

```bash
# Stop the React app: Press Ctrl+C in the frontend terminal

# Stop the API server: Press Ctrl+C in the backend terminal

# If port is still in use, find and kill the process:
lsof -ti:5001  # Find process ID using port 5001
kill -9 <PID>  # Kill the process with the returned PID
```

## 📚 API Documentation

### Photo Search Endpoints

#### POST `/agent`

Analyze photo search query with intelligent agent.

**Request:**

```json
{
  "text": "ჩემს საქაღალდეში მიპოვე სამი ფოტო რომელშიც ნათლად ჩანს კაცი და ქალი"
}
```

**Response:**

```json
{
  "success": true,
  "result": {
    "original": "ჩემს საქაღალდეში მიპოვე სამი ფოტო რომელშიც ნათლად ჩანს კაცი და ქალი",
    "is_photo_search": true,
    "photo_count": 3,
    "simplified_query": "კაცი და ქალი",
    "processing_type": "simplify_pipeline"
  }
}
```

#### GET `/pictures`

Get available pictures from the database.

**Response:**

```json
{
  "pictures": [
    {
      "name": "sunset_beach.jpg",
      "type": "nature",
      "tags": ["sunset", "beach", "ocean"]
    }
  ],
  "total": 12
}
```

### Other Endpoints

- `GET /health` - Health check
- `POST /simplify` - Simplify text to search terms
- `POST /translate` - Translate to English
- `POST /pipeline/simplify` - Run simplify pipeline
- `GET /styles` - Get available styles
- `GET /examples` - Get example texts

## 🎯 Usage Examples

### Command Line Interface

#### Photo Agent Analysis

```bash
python -m prompt_enhancer "ჩემს საქაღალდეში მიპოვე სამი ფოტო რომელშიც ნათლად ჩანს კაცი და ქალი" --agent
```

#### Pipeline Processing

```bash
python -m prompt_enhancer "ამ ფოტოებიდან მიპოვე ცხენის ფოტო რომელეც კაც ზის" --simplify-pipeline
```

### Python API Usage

```python
from prompt_enhancer.georgian_corrector import process_photo_prompt

# Photo agent analysis
result = process_photo_prompt("ჩემს საქაღალდეში მიპოვე სამი ფოტო რომელშიც ნათლად ჩანს კაცი და ქალი")
print(f"Photo count: {result['photo_count']}")
print(f"Simplified: {result['simplified_query']}")
```

## 🎨 Frontend Features

- **Modern UI**: Beautiful, responsive design with gradient backgrounds
- **Search Process Visualization**: Real-time step-by-step search process display
- **Picture Gallery**: Browse available pictures with metadata
- **Example Buttons**: Pre-filled Georgian examples for easy testing
- **Statistics Display**: Visual feedback on search analysis
- **Loading States**: Smooth animations and progress indicators
- **Error Handling**: Graceful error handling and user feedback

## 📊 Photo Agent Intelligence

The photo agent can intelligently analyze Georgian queries and:

1. **Detect Photo Search Intent**: Identifies if the query is asking for photos
2. **Extract Photo Count**: Recognizes numbers in Georgian (ერთი, ორი, სამი, etc.) and digits (1, 2, 3, etc.)
3. **Simplify Queries**: Removes unnecessary words and extracts core search terms
4. **Handle Complex Patterns**: Understands "ცალი" (pieces), plural forms, and various query structures

### Examples:

- `"ჩემს საქაღალდეში მიპოვე ფოტო"` → 1 photo
- `"ჩემს საქაღალდეში მიპოვე ფოტოები"` → 5 photos (default plural)
- `"ჩემს საქაღალდეში მიპოვე სამი ფოტო"` → 3 photos
- `"მზის 11 ცალი ფოტო მიპოვე"` → 11 photos

## 🛠️ Development

### Project Structure

```
picturesearch/
├── prompt_enhancer/          # Python AI processing modules
│   ├── georgian_corrector.py # Main correction logic
│   ├── gemini_client.py      # Gemini AI integration
│   ├── api.py               # API wrapper functions
│   └── cli.py               # Command line interface
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   └── App.css         # Styling
│   └── package.json        # Frontend dependencies
├── api_server.py           # Flask API server
├── .env                    # Environment variables
└── README.md              # This file
```

### Adding New Features

1. **New Search Functionality**: Add to `georgian_corrector.py` PhotoAgent class
2. **New API Endpoint**: Add to `api_server.py` with corresponding route
3. **Frontend Feature**: Update `frontend/src/App.js` with new UI components

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Google Gemini API key is correctly set in `.env`
2. **CORS Issues**: Make sure Flask-CORS is installed and enabled
3. **Environment Issues**: Activate the virtual environment before running Python commands
4. **Port Conflicts**: Ensure ports 3000 (React) and 5001 (Flask API) are available

### Port Management

#### Port 5001 Already in Use

```bash
# Find what's using port 5001
lsof -ti:5001

# Kill the process
kill -9 <PID>

# Alternative: Use a different port
python api_server.py --port 5002
```

#### Port 3000 Already in Use

```bash
# React will prompt to use a different port, or manually specify:
PORT=3001 npm start
```

### Environment Variables Not Loading

If you see the wrong API key in error messages, check for system-level environment variables:

```bash
echo $GOOGLE_API_KEY  # Should match your .env file
unset GOOGLE_API_KEY  # If different from .env, unset it
```

### Virtual Environment Issues

```bash
# Ensure virtual environment is active
source venv/bin/activate

# Reinstall dependencies if needed
pip install -r requirements.txt
```

### Pictures Not Loading

1. **Check Data Folder**: Ensure `data/` folder exists in the root directory
2. **File Permissions**: Make sure image files are readable
3. **Supported Formats**: Use .jpg, .jpeg, .png, or .gif files
4. **File Names**: Avoid special characters in filenames

### API Connection Issues

1. **Backend Running**: Ensure `python api_server.py` is running without errors
2. **CORS Configuration**: Flask-CORS should be properly installed
3. **Network**: Check that `http://localhost:5001/health` returns a successful response

### Frontend Build Issues

```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# If still having issues, check Node.js version
node --version  # Should be 14+
```

## 📁 Project File Structure

```
picturesearch/
├── data/                    # Picture database (create this folder)
│   ├── image1.jpg          # Your image files go here
│   ├── image2.png
│   └── ...
├── prompt_enhancer/         # Python AI processing modules
│   ├── georgian_corrector.py # Main correction logic
│   ├── gemini_client.py     # Gemini AI integration
│   ├── api.py              # API wrapper functions
│   └── cli.py              # Command line interface
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── App.css        # Styling
│   ├── public/
│   └── package.json       # Frontend dependencies
├── api_server.py          # Flask API server
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Complete Setup Script

For a quick setup, run these commands in sequence:

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Create data folder for pictures
mkdir data

# 4. Create .env file with nano editor
nano .env
# Copy the template from above and add your Google Gemini API key
# Save with Ctrl+X, then Y, then Enter

# 5. Setup frontend
cd frontend
npm install
cd ..

# 6. Start backend (in one terminal)
python api_server.py

# 7. Start frontend (in another terminal)
cd frontend && npm start
```

### Environment Variables Not Loading

If you see the wrong API key in error messages, check for system-level environment variables:

```bash
echo $GOOGLE_API_KEY  # Should match your .env file
unset GOOGLE_API_KEY  # If different from .env
```

## 📄 License

This project is part of the picturesearch application and follows the same license terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For issues and questions, please open an issue on the repository or contact the development team.
