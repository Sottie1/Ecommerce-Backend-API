from fastapi import FastAPI
from routers import orders, products, users, auth, cart, utility
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(utility.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="E-commerce API",
        version="1.0.0",
        description="This is an Ecommerce API.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/api/v1/")
async def root():
    return {"message": "Welcome to our Ecommerce Backend!"}

