from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.equipment import EquipmentSchema, EquipmentCreateSchema
from crud.equipment import create_equipment, get_equipment, get_all_equipment, update_equipment, delete_equipment
from database import get_db

router = APIRouter()

@router.post("/equipment", response_model=EquipmentSchema)
def create_new_equipment(equipment: EquipmentCreateSchema, db: Session = Depends(get_db)):
    return create_equipment(db, equipment)

@router.get("/equipment/{equipment_id}", response_model=EquipmentSchema)
def read_equipment(equipment_id: int, db: Session = Depends(get_db)):
    db_equipment = get_equipment(db, equipment_id)
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return db_equipment

@router.get("/equipment", response_model=list[EquipmentSchema])
def read_all_equipment(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_equipment(db, skip=skip, limit=limit)

@router.put("/equipment/{equipment_id}", response_model=EquipmentSchema)
def update_existing_equipment(equipment_id: int, equipment: EquipmentSchema, db: Session = Depends(get_db)):
    db_equipment = update_equipment(db, equipment_id, equipment)
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return db_equipment

@router.delete("/equipment/{equipment_id}", response_model=EquipmentSchema)
def delete_equipment_by_id(equipment_id: int, db: Session = Depends(get_db)):
    db_equipment = delete_equipment(db, equipment_id)
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return db_equipment
