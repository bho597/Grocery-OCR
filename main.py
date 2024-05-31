from fastapi import FastAPI

from api.postgres_models.receipts import Base
from api.config.postgresql import engine
from api.routes.receiptsRoute import receiptsRoute
from api.routes.defaultRoute import defaultRoute

app = FastAPI(title="Grocery OCR", description="Grocery Receipt CRUD API")

Base.metadata.create_all(bind= engine)


app.include_router(receiptsRoute,tags=['Receipts'], prefix='/api/receipts')
app.include_router(defaultRoute)

