from fastapi import APIRouter, Depends, HTTPException
from .. import database, schemas, models
from sqlalchemy.orm import Session
import register
from fastapi import APIRouter, Depends, status
from .. import schemas, database, models, oAuth2
from sqlalchemy.orm import Session


router = APIRouter(tags=["Users"])
get_db = database.get_db


@router.post("/register-user", response_model=schemas.User)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    ch = db.query(models.User).filter(models.User.email == request.email).first()
    if not ch:
        new_user = models.User(
            name=request.name, email=request.email, password=request.password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        register.take_photos(new_user.id)
        return new_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User aldready exists",
        )
