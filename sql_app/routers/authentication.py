from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, token
from face_recognition.testing import test


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    request: schemas.Login,
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User).filter(models.User.email == request.email).first()
    )  # Use .first() to retrieve the user object
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid username"
        )
    if user.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password"
        )
    get_id = user.id
    # usernames = db.query(models.User.name).all()
    # name_list = [username[0] for username in usernames]
    # check = test(get_id, name_list)
    # if check != 1:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail=f"Unrecognised User"
    #     )
    info = db.query(models.Info).filter(models.Info.user_id == get_id).first()
    if not info:
        return {"id": get_id, "ch": 1}
    else:
        return {"id": get_id, "ch": 0}
