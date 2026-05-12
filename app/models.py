from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="client")


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    car_model = Column(String)
    plate_number = Column(String, unique=True)
    rating = Column(Float, default=5.0)


class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    multiplier = Column(Float)


class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True)
    pickup = Column(String)
    destination = Column(String)
    price = Column(Float)
    status = Column(String, default="created")

    user_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    tariff_id = Column(Integer, ForeignKey("tariffs.id"))

    user = relationship("User")
    driver = relationship("Driver")
    tariff = relationship("Tariff")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    method = Column(String)
    status = Column(String)

    ride_id = Column(Integer, ForeignKey("rides.id"))


class Tracking(Base):
    __tablename__ = "tracking"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)

    ride_id = Column(Integer, ForeignKey("rides.id"))