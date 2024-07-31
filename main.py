from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import info, users, authentication
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import register


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Update with the appropriate origin URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(engine)

app.include_router(info.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.mount("/static", StaticFiles(directory="sql_app/static"), name="static")


@app.get("/")
def index():
    with open("frontend/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/check-user")
def check_user():
    proceed = register.live_check()
    if proceed == 1:
        proceed = register.gender_check()
        if proceed == 1:
            return {"success": "True"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add user.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add user.",
        )


# @app.get("/check-user")
# def check_user():
#     proceed = register.gender_check()
#     if proceed == 1:
#         return {"success": "True"}
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to add user.",
#         )