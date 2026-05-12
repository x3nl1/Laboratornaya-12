from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class DriverCreate(BaseModel):
    name: str
    car_model: str
    plate_number: str


class RideCreate(BaseModel):
    pickup: str
    destination: str
    price: float
    user_id: int
    driver_id: int
    tariff_id: int