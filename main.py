import uvicorn

from app.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, log_level="info", reload=True)
