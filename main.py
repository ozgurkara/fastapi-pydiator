import uvicorn

from app.application import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app)
    #uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", use_colors=True)
