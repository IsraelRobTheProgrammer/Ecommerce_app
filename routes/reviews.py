from fastapi import Path, status, HTTPException, Depends, APIRouter
from models.review import Review
from auth import verify_token
from sql_database import get_db
from sqlalchemy.orm import Session
from typing import List
from schema_val import Review_Req, Review_Res
from typing import Optional

router = APIRouter(
    prefix="/review",
    tags=["Review"]
)


@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=Review_Res)
def add_review(id: int, review_req: Review_Req, db: Session = Depends(get_db), current_user_data=Depends(verify_token)):
    try:
        user_id = current_user_data.user_id
        new_review = Review(user_id=user_id, item_id=id, **review_req.dict())
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"You've Already Reviewed This Product")
