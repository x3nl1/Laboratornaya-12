from pydantic import BaseModel, EmailStr, Field


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
    price: float = Field(gt=0)
    user_id: int
    driver_id: int
    tariff_id: int