from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# localhost:8000/
@app.get("/")
async def home(request: Request):
    data = "hello my project"
    return templates.TemplateResponse("index.html", {"request": request, "data" : data})
# localhost:8000/dashboard
@app.get("/dashboard")
async def dashboard(request: Request):
    data = "hello my project"
    return templates.TemplateResponse("dashboard.html", {"request": request, "data" : data})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
