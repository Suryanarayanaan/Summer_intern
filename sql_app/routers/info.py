from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .. import schemas, database, models, oAuth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from .. import database, schemas, models, oAuth2
import random

router = APIRouter(tags=["Info"])
templates = Jinja2Templates(directory="sql_app/templates")

get_db = database.get_db


@router.post("/add-details", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Info, db: Session = Depends(get_db)):
    while True:
        no = random.randint(pow(10, 9), pow(10, 10) - 1)
        if not db.query(models.Info).filter(models.Info.app_no == no).first():
            break

    new_info = models.Info(
        name=request.name,
        inst_name=request.inst_name,
        course_name=request.course_name,
        annual_income=int(request.annual_income),
        community=request.community,
        app_no=no,
        user_id=int(request.user_id),
    )
    db.add(new_info)
    db.commit()
    db.refresh(new_info)
    print(new_info.app_no)
    return new_info.app_no


@router.get("/info/{id}", status_code=200)
def show(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
):
    blog = db.query(models.Info).filter(models.Info.user_id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No information found for id : {id} ",
        )
    return templates.TemplateResponse(
        "submit.html",
        {
            "request": request,
            "app_no": blog.app_no,
            "name": blog.name,
            "inst_name": blog.inst_name,
            "course_name": blog.course_name,
            "annual_income": blog.annual_income,
            "community": blog.community,
            "user_id": blog.user_id,
        },
    )
