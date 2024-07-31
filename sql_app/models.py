from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Info(Base):
    __tablename__ = "info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    inst_name = Column(String)
    course_name = Column(String)
    annual_income = Column(Integer)
    community = Column(String)
    app_no = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key relationship

    user = relationship("User", back_populates="info")  # Relationship with User table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    info = relationship("Info", back_populates="user")  # Relationship with Info table
