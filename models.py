from sqlalchemy import Column, Integer, Float, String, Boolean
from database import Base

# Sales 모델 정의
class Sales(Base):
    __tablename__ = 'sales'  # 테이블 이름
    
    id = Column(Integer, primary_key=True, index=True)
    sales_amount = Column(Float, nullable=False)  # 매출액
    month = Column(String(2), nullable=False)  # 월

# Todo 모델 정의
class Todo(Base):
    __tablename__ = "todos"  # 테이블 이름
    
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255), nullable=False)  # 할일(task) 설명
    completed = Column(Boolean, default=False)  # 완료 여부
