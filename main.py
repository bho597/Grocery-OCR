from fastapi import FastAPI

from api.postgres_models.receipts import Base
from api.config.postgresql import engine

from api.routes.receipts_route import receiptsRoute
from api.routes.line_items_route import lineItemsRoute
from api.routes.calculate_route import calculateRoute
from api.routes.default_route import defaultRoute


app = FastAPI(title="Grocery OCR", description="Grocery Receipt CRUD API")

Base.metadata.create_all(bind= engine)


app.include_router(receiptsRoute,tags=['Receipts'], prefix='/api')
app.include_router(lineItemsRoute,tags=['Line Items'], prefix='/api')
app.include_router(calculateRoute,tags=['Calculate'], prefix='/api')
app.include_router(defaultRoute)

