from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String(255), nullable=False)
    equipment_type = Column(String(255), nullable=True)
    count = Column(Integer, default=0, nullable=False)
    equipment_description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Adding user_id as foreign key
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="equipments")
