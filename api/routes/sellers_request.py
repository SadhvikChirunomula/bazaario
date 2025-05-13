from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.models.sellers_request import SellersRequest
from api.schemas.sellers_request import SellersRequestSchema

router = APIRouter()

@router.get("/sellers_requests", response_model=list[SellersRequestSchema])
def get_sellers_requests(db: Session = Depends(get_db)):
    return db.query(SellersRequest).all()