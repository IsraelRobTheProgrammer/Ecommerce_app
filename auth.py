from jose import JWTError, jwt
from datetime import datetime, timedelta
from schema_val import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.user import User

from config import settings as st


from sql_database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = f"{st.secret_key}"
ALGORITHM = f"{st.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = int(f"{st.access_token_expire_minutes}")


def create_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_data = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_data


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = payload.get("user_id")
        if id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could Not Validate Credentials, Please Login",
                headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(user_id=user_id)
    except JWTError as error:
        print("An error has occurred", error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could Not Validate Credentials, Please Login",
            headers={"WWW-Authenticate": "Bearer"})

    return token_data


def get_current_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    return user


# def check_user_access(id: int, current_user: int):
#     if(id != current_user):
#         return False
#     return True
