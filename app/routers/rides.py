from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import RideCreate
from app.models import Ride, User, Driver, Tariff

router = APIRouter(prefix="/rides", tags=["rides"])


@router.post("/")
def create_ride(ride: RideCreate, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == ride.user_id).first():
        raise HTTPException(404, "User not found")
    if not db.query(Driver).filter(Driver.id == ride.driver_id).first():
        raise HTTPException(404, "Driver not found")
    if not db.query(Tariff).filter(Tariff.id == ride.tariff_id).first():
        raise HTTPException(404, "Tariff not found")
    db_ride = Ride(**ride.dict())
    db.add(db_ride)
    db.commit()
    return db_ride


@router.get("/")
def get_rides(db: Session = Depends(get_db)):
    return db.query(Ride).all()


@router.put("/{ride_id}")
def update_ride(ride_id: int, status: str, db: Session = Depends(get_db)):
    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(404, "Ride not found")

    ride.status = status
    db.commit()

    return ride


@router.delete("/{ride_id}")
def delete_ride(ride_id: int, db: Session = Depends(get_db)):
    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(404, "Ride not found")

    db.delete(ride)
    db.commit()

    return {"message": "deleted"}