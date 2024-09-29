from sqlalchemy.orm import Session
from models.equipment import Equipment
from schemas.equipment import EquipmentSchema

def create_equipment(db: Session, equipment: EquipmentSchema):
    db_equipment = Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

def get_equipment(db: Session, equipment_id: int):
    return db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()

def get_all_equipment(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Equipment).offset(skip).limit(limit).all()

def update_equipment(db: Session, equipment_id: int, equipment: EquipmentSchema):
    db_equipment = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()
    if db_equipment:
        for key, value in equipment.dict().items():
            setattr(db_equipment, key, value)
        db.commit()
        db.refresh(db_equipment)
    return db_equipment

def delete_equipment(db: Session, equipment_id: int):
    db_equipment = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()
    if db_equipment:
        db.delete(db_equipment)
        db.commit()
    return db_equipment
