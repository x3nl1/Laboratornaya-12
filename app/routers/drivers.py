from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Driver
from app.schemas import DriverCreate

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/")
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    db_driver = Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    return db_driver


@router.get("/")
def get_drivers(db: Session = Depends(get_db)):
    return db.query(Driver).all()