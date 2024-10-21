from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, StreamingResponse
from sqlalchemy.orm import Session
import uvicorn
from face_recog import FaceRecog, video_process
import models
from database import engine, SessionLocal
from models import Todo  # Import Todo model


# Initialize database models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Static and template directories setup
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### Sales and Dashboard Functionality ###
# Fetch sales data
def get_sales_data():
    with SessionLocal() as session:
        return session.query(models.Sales.month, models.Sales.sales_amount).all()

def update_sales_by_month(month, sales_amount):
    with SessionLocal() as session:
        month_str = str(month).zfill(2)
        existing_sale = session.query(models.Sales).filter(models.Sales.month == month_str).first()
        if existing_sale:
            existing_sale.sales_amount = sales_amount
            session.commit()
        else:
            new_sale = models.Sales(month=month_str, sales_amount=sales_amount)
            session.add(new_sale)
            session.commit()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": "hello my project"})

@app.get("/dashboard")
async def dashboard(request: Request):
    sales_data = get_sales_data()
    month = [item.month for item in sales_data]
    sales_amount = [item.sales_amount for item in sales_data]

    growth_rate = [((sales_amount[i] - sales_amount[i-1]) / sales_amount[i-1]) * 100 for i in range(1, len(sales_amount))]
    growth_rate.insert(0, 0)

    while len(month) > 12:
        month.pop()
        sales_amount.pop()
        growth_rate.pop()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "month": month,
        "sales_amount": sales_amount,
        "growth_rate": growth_rate
    })

@app.post("/save_data")
async def save_data(request: Request, month: int = Form(...), sales_amount: int = Form(...)):
    update_sales_by_month(month, sales_amount)
    return RedirectResponse(url='/dashboard', status_code=303)

### ToDo App Functionality ###
@app.get("/todo")
async def todo_home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    print(todos)  # 이 줄을 추가하여 데이터가 제대로 가져와지는지 확인
    return templates.TemplateResponse("todo_index.html", {
        "request": request,
        "todos": todos,
    })

@app.post("/add")
async def add_task(task: str = Form(...), db: Session = Depends(get_db)):
    new_todo = Todo(task=task)
    db.add(new_todo)
    db.commit()
    return RedirectResponse(url="/todo", status_code=303)

@app.get("/edit/{id}")
async def edit_task(id: int, request: Request, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    todos = db.query(Todo).all()
    return templates.TemplateResponse("todo_edit.html", {"request": request, "todo": todo, "todos": todos})

@app.post("/edit/{id}")
async def update_task(id: int, task: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo:
        todo.task = task
        todo.completed = completed
        db.commit()
    return RedirectResponse(url="/todo", status_code=303)

@app.get("/delete/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url="/todo", status_code=303)

### Face Recognition Functionality ###
@app.get("/face_recog_view")
async def face_recog_view(request: Request):
    return templates.TemplateResponse("face_recog.html", {"request": request})

@app.get("/face_recog")
def face_recog():
    face_recog_instance = FaceRecog()
    return StreamingResponse(video_process(face_recog_instance), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
print(todos)  # 이 줄을 통해 데이터가 제대로 가져와지는지 확인
