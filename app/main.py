
from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes import zones
from app.routes import slots


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
