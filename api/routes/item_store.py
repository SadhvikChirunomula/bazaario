from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.models.item_store import ItemStore
from api.schemas.item_store import ItemStoreSchema

router = APIRouter()

@router.get("/items_store", response_model=list[ItemStoreSchema])
def get_items_store(db: Session = Depends(get_db)):
    return db.query(ItemStore).all()