import sys
import base64

from fastapi import FastAPI, File, UploadFile, HTTPException

from api.model.receipt_model import Base
from api.config.postgresql import engine

app = FastAPI()

Base.metadata.create_all(bind= engine)

@app.get("/")
# takes a query parameter name
async def root():
    return {"message": f"Welcome to the Grocery OCR API."}


# @app.post("/upload/")
# async def upload_image(file: UploadFile = File(...)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=415, detail="Unsupported Media Type. Only images are allowed.")

#     # Read the content of the uploaded file
#     content = await file.read()
#     encoded_content = base64.b64encode(content)
#     encoded_content_str = encoded_content.decode("utf-8")

#     return {"content": encoded_content_str}



@app.get("/health")
async def health():
    return {"status": "healthy"}
