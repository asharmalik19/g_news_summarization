import uvicorn

from app.downloader import download_db

def main():
    download_db()
    uvicorn.run('app.main:app', port=8000, log_level='info')

if __name__ == "__main__":
    main()
