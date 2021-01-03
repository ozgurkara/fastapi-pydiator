import uvicorn

from app.app import create_app

app = create_app()


print(__name__)
if __name__ == "__main__":
    uvicorn.run(app)
    # uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
