from pydantic import BaseModel

class EquipmentSchema(BaseModel):
    equipment_name: str
    equipment_type: str = None
    count: int
    equipment_description: str = None
    user_id: int  # Add user_id to the schema

    class Config:
        orm_mode = True

class EquipmentCreateSchema(BaseModel):
    equipment_name: str
    equipment_type: str = None
    count: int
    equipment_description: str = None
    user_id: int  # Add user_id here too

    class Config:
        orm_mode = True
