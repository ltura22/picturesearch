# Photo Search Agent - Georgian AI

A full-stack AI-powered application for searching and analyzing pictures using natural language queries in Georgian.

## Photo Intelligence

The application's photo intelligence operates through two core phases: an initial data preprocessing stage and a sophisticated, real-time search process. This dual approach ensures that user queries in Georgian are deeply understood and that the most relevant images are retrieved with high accuracy.

### Data Preprocessing and Storage

To build a searchable and intelligent image database, the system first processes and indexes the entire collection of pictures. This foundational stage consists of several automated steps:

1.  **Image Description Generation**: For each picture in the source folder, the system employs the BLIP (Bootstrapping Language-Image Pre-training) model to generate a rich, accurate description of the visual content.

2.  **Translation to Georgian**: The English descriptions from BLIP are then translated into Georgian using Facebook's high-performance NLLB (No Language Left Behind) model, ensuring linguistic accuracy.

3.  **Database and Vector Storage**: The translated Georgian descriptions are stored in a primary database. To enable semantic understanding, these descriptions are also converted into numerical vector embeddings using the `paraphrase-multilingual-MiniLM-L12-v2` model. These vectors, which capture the contextual meaning of the text, are stored in a FAISS (Facebook AI Similarity Search) vector database for rapid similarity lookups.

4.  **BM25 Model Fitting**: Concurrently, a BM25 (Best Matching 25) model, a state-of-the-art keyword-based ranking algorithm, is fitted on the tokenized Georgian text descriptions. This prepares a separate retrieval mechanism optimized for lexical matching.

### Prompt Engineering and Hybrid Search

When a user submits a search query, the system initiates a multi-layered process to analyze the request and retrieve the best results:

1.  **Prompt Analysis with Gemini**: The user's prompt is first sent to Gemini for advanced natural language understanding. This step achieves two goals:
    *   **Quantity Extraction**: It intelligently identifies the number of photos the user is asking for. If not specified, it defaults to one for singular nouns (e.g., "ფოტო") and five for plural nouns (e.g., "ფოტოები").
    *   **Query Simplification**: It distills the user's natural language query into a simplified set of core search terms, dropping unnecessary words to align with the style of the stored database descriptions.

2.  **Hybrid Search Execution**: The system then performs two types of searches simultaneously to leverage the strengths of different retrieval methods:
    *   **BM25 Keyword Search**: The simplified query is used to score all pictures in the database based on BM25's term-frequency relevance algorithm.
    *   **FAISS Vector Search**: Using the query's vector embedding, the system performs a cosine-similarity search in the FAISS database to retrieve the `2*k` most semantically related images (where `k` is the number of photos requested).

3.  **Result Merging and Ranking**: To generate the final output, the system merges results by taking the top `2k` images from the FAISS vector search, calculating a hybrid score for each by combining its BM25 keyword score (80% weight) with its FAISS similarity score (20% weight), and then selects the final `k` images with the highest-ranked scores.

## Installation & Setup

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

## Running the Application

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
