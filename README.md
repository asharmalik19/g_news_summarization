![WIP](https://img.shields.io/badge/status-WIP-yellow.svg)

# Google News Summarizer
A Python application that extracts news articles from Google News feeds and generates concise summaries using Large Language Models (LLM).

## Features
- 📰 Extracts news articles from Google News RSS feeds
- 🤖 Generates concise summaries using LLM
- 🌐 Web interface to display summaries with source links
- 📂 Browse news summaries by category
- 🔄 Fresh news updates via downloadable database

## Prerequisites
- **Python 3.12+**
- Internet connection for downloading news database

## Installation
1. Clone the repo:
    ```bash
    git clone https://github.com/asharmalik19/g_news_summarization.git
    cd g_news_summarization
    ```
2. Create & activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    ```
3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Navigate to the app folder and download the updated database file by running
    ```bash
    python3 ./download_db.py
    ```

## Usage
1. **Navigate to the app folder**

2. **Start the application by running**
   ```bash
   uvicorn main:app --port 8000     # or any other free port
   ```

3. **Open your browser and navigate to**
   ```
   http://127.0.0.1:8000
   ```

**Note:** You need to download the fresh copy of sqlite db file before running the application to get the fresh news articles.


