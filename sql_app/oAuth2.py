from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import token, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    data: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    payload = token.verify_token(data)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
