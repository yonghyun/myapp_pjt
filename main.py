from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
import uvicorn
import models
from database import engine, SessionLocal
from fastapi.responses import RedirectResponse

app = FastAPI()

# 데이터베이스 초기화
models.Base.metadata.create_all(bind=engine)

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

# 데이터베이스에서 데이터를 가져오는 함수
def get_sales_data():
    with SessionLocal() as session:
        results = session.query(models.Sales.month, models.Sales.sales_amount).all()
    return results

def update_sales_by_month(month, sales_amount):
    with SessionLocal() as session:
        try:
            # month 값을 두 자리 문자열로 변환 ("1" -> "01")
            month_str = str(month).zfill(2)  # 1 -> "01"로 변환
            print(f"업데이트할 월: {month_str}, 업데이트할 매출액: {sales_amount}")
            
            # 변환된 문자열을 기준으로 검색
            existing_sale = session.query(models.Sales).filter(models.Sales.month == month_str).first()

            if existing_sale:
                existing_sale.sales_amount = sales_amount
                session.commit()
                session.refresh(existing_sale)
            else:
                # 해당 월에 데이터가 없을 경우 새로 추가
                new_sale = models.Sales(month=month_str, sales_amount=sales_amount)
                session.add(new_sale)
                session.commit()
                session.refresh(new_sale)
                print(f"새로운 데이터 추가: {new_sale.month}월, 매출액: {new_sale.sales_amount}")
        except Exception as e:
            session.rollback()
            print(f"데이터 업데이트 중 오류 발생: {e}")
        finally:
            session.close()


# 메인 페이지 엔드포인트
@app.get("/")
async def home(request: Request):
    data = "hello my project"
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

@app.get("/face")
async def face(request: Request):
    data3 = "face_recognition"
    return templates.TemplateResponse("face_reco.html", {"request": request, "data3": data3})


# 대시보드 페이지 엔드포인트
@app.get("/dashboard")
async def dashboard(request: Request):
    data1 = "Welcome to the Dashboard"
    sales_data = get_sales_data()
    month = [item.month for item in sales_data]
    sales_amount = [item.sales_amount for item in sales_data]

    # 증감률 계산
    growth_rate = []
    for i in range(1, len(sales_amount)):
        rate = ((sales_amount[i] - sales_amount[i-1]) / sales_amount[i-1]) * 100
        growth_rate.append(rate)
    growth_rate.insert(0, 0)

    # 잘못된 데이터 포인트 삭제 (e.g. "1,1,1" 부분)
    while len(month) > 12:  # 월이 12를 초과하는 경우만 삭제
        month.pop()
        sales_amount.pop()
        growth_rate.pop()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "data1": data1,
        "month": month,
        "sales_amount": sales_amount,
        "growth_rate": growth_rate
    })

# 데이터 저장 엔드포인트
@app.post("/save_data")
async def save_data(request: Request, month: int = Form(...), sales_amount: int = Form(...)):
    # 기존 데이터 업데이트
    update_sales_by_month(month, sales_amount)

    # URL 리디렉션을 명시적으로 처리
    return RedirectResponse(url='/dashboard', status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
