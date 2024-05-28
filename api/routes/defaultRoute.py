from fastapi import APIRouter
from fastapi.responses import FileResponse

from api.config.settings import Settings


defaultRoute = APIRouter()

@defaultRoute.get('/')
async def root():
    return {"message": f"Welcome to the Grocery OCR API."}

@defaultRoute.get("/health")
async def health():
    return {"status": "healthy"}


favicon_path = "./static/images/receipt_icon.ico"


@defaultRoute.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse(favicon_path)