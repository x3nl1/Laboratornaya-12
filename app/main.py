from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, drivers, rides, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Taxi Service API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(drivers.router)
app.include_router(rides.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "Taxi Service API"}