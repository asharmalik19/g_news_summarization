# Google News Summarizer
A Python application that extracts news articles from Google News feeds and generates concise summaries using a Large Language Model (LLM), giving you daily fresh summaries by topics (i.e, Technology, Business etc).

## Features
- 📰 Extracts news articles from Google News RSS feeds
- 🤖 Generates concise summaries using LLM
- 🌐 Web interface to display summaries with source links
- 📂 Browse news summaries by category
- 🔄 Fresh news updates via downloadable database
- 🔍 RAG based search functionality where you can get a summarized content based on a query

## Prerequisites
- Python 3.12+
- Internet connection for downloading news database
- Gemini API key (for the search functionality)

Get your Gemini API key from the Google AI Studio.

## Setup guide
1. Clone the repo:
    ```bash
    git clone https://github.com/asharmalik19/g_news_summarization.git
    cd g_news_summarization
    ```
2. Create a `.env` file in the root directory of the project and this line to the file:
    ```bash
    GEMINI_API_KEY=your_gemini_api_key_here
    ```
   Replace `your_gemini_api_key_here` with your actual Gemini API key.

3. Create & activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    ```
4. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Download the updated database files by running
    ```bash
    python app/download_db.py
    ```
This will download the latest `articles_data.db` file and `chroma_db` from the releases of this repo and place it in the `data` folder.

## Usage
1. **Start the application by running**
   ```bash
   uvicorn app.main:app --port 8000     # or any other free port
   ```

2. **Open your browser and navigate to**
   ```
   http://127.0.0.1:8000
   ```

**Note:** You need to download the fresh copy of sqlite db file before running the application to get the daily fresh news articles.

## Project Structure
```
├── .github
│   └── workflows
├── .gitignore
├── LICENSE
├── README.md
├── app
│   ├── download_db.py
│   └── main.py
├── data
│   └── articles_data.db
├── data_extraction_pipeline
│   ├── generate_summary.py
│   └── get_data.py
├── rag
│   └── embedding_function.py
|   |── generate_embeddings.py
|   |── rag_search.py  
├── requirements.txt
├── static
│   └── index.html
└── venv
```

## Data Extraction 
A github actions workflow is set to run the data extraction pipeline daily which contains `get_data.py` and `generate_summary.py` scripts. The final output of this pipeline is a `sqlite` database file. The workflow adds this database file to the releases of this repo replacing the previous file. 

This is how the database containing news articles and their generated summaries is updated daily but if you want the most recent articles, then you can run the workflow manually which runs the data extraction pipeline.






