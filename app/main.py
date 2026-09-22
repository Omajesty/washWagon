
from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes import zones
from app.routes import slots
from app.routes import users
from app.routes import orders
from app.routes import price_list


app = FastAPI(
    title="washWagon API",
    description="Laundry pickup and delivery service API",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {
        "message": "washWagon API is running"
    }
    
app.include_router(auth_router)
app.include_router(zones.router)
app.include_router(slots.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(price_list.router)
