
from fastapi import FastAPI


def create_app():
    app = FastAPI()
    return app

app = create_app()

@app.get("/content-workflow")
def get_content_workflow():
    return {"Hello": "World"}