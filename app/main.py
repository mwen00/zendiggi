from fastapi import FastAPI, APIRouter, status, Request, Depends, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates

import os
from dotenv import load_dotenv

from pathlib import Path
from sqlalchemy.orm import Session

from app.clients.google import query_google, insert_location
from app import deps
from app import crud


# TODO: Remove once the FE is in place
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

# load env
load_dotenv()

# Not sure I need to specify this param `openapi_url`
app = FastAPI(title="Zendiggi API", openapi_url="/openapi.json")

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def root(request: Request) -> dict:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "message": "Hello, World!"}
    )


@router.post("/process-location/", status_code=status.HTTP_202_ACCEPTED)
def process_location(background_tasks: BackgroundTasks, location: str = Form()) -> dict:
    """
    Acknowledges location input client and starts scraping process
    """
    background_tasks.add_task(query_google, location)

    return {"message": f"Scraping for {location} has been submitted successfully."}


app.include_router(router)


if __name__ == "__main__":
    # For debugging only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
