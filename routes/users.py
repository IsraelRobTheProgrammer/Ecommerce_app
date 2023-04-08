from fastapi import Path, status, HTTPException, Depends, APIRouter
from sql_database import get_db
from models.user import User
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from auth import create_token
from fastapi.security import OAuth2PasswordRequestForm
from schema_val import User_Req, User_Res, Token

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{id}", response_model=User_Res)
def get_user(db: Session = Depends(get_db), id: int = Path(gt=0)):
    user = db.query(User).filter(User.user_id == id).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user


@router.post("/auth/register", status_code=status.HTTP_201_CREATED, response_model=User_Res)
def create_user(user_req: User_Req, db: Session = Depends(get_db)):

    hashed_password = pwd_context.hash(user_req.password)
    user_req.password = hashed_password
    new_user = User(**user_req.dict())
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/auth/login", status_code=status.HTTP_200_OK, response_model=Token)
def login_user(user_req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_req.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User Does Not Exist")

    if not pwd_context.verify(user_req.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Username or password Incorrect"
        )
    # Create access token
    access_token = create_token(data={"user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
