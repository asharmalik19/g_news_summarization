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
- `uv` 
- Internet connection for downloading news database
- Gemini API key (for the search functionality)

Get your Gemini API key from the Google AI Studio.

## Setup guide
1. Install `uv` from here: https://docs.astral.sh/uv/getting-started/installation/

2. Clone the repo:
    ```bash
    git clone https://github.com/asharmalik19/g_news_summarization.git
    cd g_news_summarization
    ```
3. Create a `.env` file in the root directory of the project and this line to the file:
    ```bash
    GEMINI_API_KEY=your_gemini_api_key_here
    ```
Replace `your_gemini_api_key_here` with your actual Gemini API key.

4. Syncronize virtual environment by installing the required packages
    ```bash
    uv sync
    ```

This will automatically download the latest `articles_data.db` file and `chroma_db` and start the app.

## Usage
1. Run the `app.py` file
    ```bash
    uv run app.py
    ```
   
    If port 8000 is busy, specify a different port:
    ```bash
    uv run main.py 8001
    ```

2. **Open your browser and navigate to**
    ```
    http://127.0.0.1:8000
    ```
    (Or whatever port you specified)

## Project Structure
```
.
├──github/
├── app.py
├── src
│   ├── g_news_summarization
│   │   ├── __init__.py
│   │   ├── downloader.py
│   │   ├── embedding_function.py
│   │   ├── generate_embeddings.py
│   │   ├── generate_summary.py
│   │   ├── get_data.py
│   │   ├── main.py
│   │   └── rag_search.py
├── data
│   ├── articles.csv
│   ├── articles_data.db
│   ├── chroma_db
├── static
│   └── index.html
├── tests
│   └── test_get_data.py
├── pyproject.toml
└── uv.lock
├── LICENSE
├── README.md
```

## Data Extraction 
A github actions workflow is set to run the data extraction pipeline daily which contains `get_data.py` and `generate_summary.py` scripts. The final output of this pipeline is a `sqlite` database file. The workflow adds this database file to the releases of this repo replacing the previous file. 

This is how the database containing news articles and their generated summaries is updated daily but if you want the most recent articles, then you can run the workflow manually which runs the data extraction pipeline.

### Next Steps
- [x] Optimize the data extraction by using `playwright asynchronous` API to render multiple urls ayncronously.
- [] Enhance the displayed summaries.

### Minor Enhancements
- [] Improve the technical docs.


