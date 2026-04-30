from fastapi import FastAPI
from app.routers import auth, projects, tasks, dashboard
from app.database import engine, Base
from app import models


app=FastAPI()

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(dashboard.router)


@app.get("/")
def read_root():
    return {"status":"ok"}

Base.metadata.create_all(bind=engine)