from fastapi import Path, status, HTTPException, Depends, APIRouter
from models.item import Item
from models.review import Review
from auth import verify_token
from sql_database import get_db
from sqlalchemy.orm import Session
from typing import List
from schema_val import Item_Req, Item_Res
from typing import Optional


router = APIRouter(
    prefix="/items",
    tags=["Item"]
)


@router.get("/", response_model=List[Item_Res])
def index(search_query: Optional[str] = None, db: Session = Depends(get_db), current_user_data=Depends(verify_token)):
    if search_query is not None:
        searched_item = db.query(Item).filter(
            Item.name.contains(search_query)).all()
        return searched_item
    else:
        items = db.query(Item).all()
        # print(items)
        return items


@router.get("/{id}", response_model=Item_Res)
def get_items(db: Session = Depends(get_db), id: int = Path(gt=0)):
    items = db.query(Item).filter(Item.item_id == id).first()
    if items == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")
    return items


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Item_Res)
def create_item(item_req: Item_Req, db: Session = Depends(get_db), current_user_data: int = Depends(verify_token)):
    new_item = Item(user_id=current_user_data.user_id, **item_req.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int = Path(gt=0), db: Session = Depends(get_db),  current_user_data: int = Depends(verify_token)):
    del_query = db.query(Item).filter(Item.item_id == id).first()
    if del_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item Not Found")

    if del_query.user_id != current_user_data.dict()["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Operation Not Allowed")

    db.query(Item).filter(
        Item.item_id == id).delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", response_model=Item_Res)
def update_item(updated_item_req: Item_Req, id: int = Path(gt=0), db: Session = Depends(get_db),  current_user_data: int = Depends(verify_token)):
    updated_query = db.query(Item).filter(Item.item_id == id)
    updated_item = updated_query.first()

    if updated_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item Not Found")

    if updated_item.user_id != current_user_data.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Operation Not Allowed")

    db.query(Item).filter(Item.item_id == id).update(
        updated_item_req.dict(), synchronize_session=False)
    db.commit()
    return updated_query.first()
