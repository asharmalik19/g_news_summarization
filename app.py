import sys

import uvicorn

from g_news_summarization.downloader import download_db

def main():
    port = 8000
    # if user provided a port number as an argument, use that one
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        
    download_db()
    uvicorn.run('g_news_summarization.main:app', port=port, log_level='info')

if __name__ == "__main__":
    main()
