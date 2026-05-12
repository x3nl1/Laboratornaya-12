from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Ride

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/rides")
def ride_stats(db: Session = Depends(get_db)):
    rides = db.query(Ride).all()

    return {
        "total_rides": len(rides),
        "total_revenue": sum(r.price for r in rides)
    }