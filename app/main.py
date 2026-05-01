from fastapi import FastAPI, Request
from app.routers import auth, projects, tasks, dashboard
from app.database import engine, Base
from app import models
from fastapi.templating import Jinja2Templates


app=FastAPI()
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(dashboard.router)




@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(request, "signup.html", {"request": request})


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})



@app.get("/projects")
def projects_page(request: Request):
    return templates.TemplateResponse(request, "projects.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):    
    return templates.TemplateResponse(request, "dashboard.html", {"request": request})  


@app.get("/projects/{project_id}")
def project_detail_page(request: Request, project_id: int):
    return templates.TemplateResponse(
        request,
        "project_detail.html",
        {"request": request, "project_id": project_id}
    )

@app.get("/projects/{project_id}/tasks/new")
def create_task_page(request: Request, project_id: int):
    return templates.TemplateResponse(
        request,
        "task_create.html",
        {"request": request, "project_id": project_id}
    )

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html",{"request": request})

Base.metadata.create_all(bind=engine)