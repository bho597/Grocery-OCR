from fastapi import FastAPI

from api.postgres_models.receipts import Base
from api.config.postgresql import engine
from api.routes.receiptsRoute import receiptsRoute
from api.routes.defaultRoute import defaultRoute

app = FastAPI(title="Grocery OCR", description="Grocery Receipt CRUD API")

Base.metadata.create_all(bind= engine)

app.include_router(receiptsRoute,tags=['Receipts'], prefix='/api/receipts')
app.include_router(defaultRoute)


# @app.post("/upload/")
# async def upload_image(file: UploadFile = File(...)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=415, detail="Unsupported Media Type. Only images are allowed.")

#     # Read the content of the uploaded file
#     content = await file.read()
#     encoded_content = base64.b64encode(content)
#     encoded_content_str = encoded_content.decode("utf-8")

#     return {"content": encoded_content_str}



