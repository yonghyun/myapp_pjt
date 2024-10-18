from sqlalchemy import Column, Integer, Float, String
from database import Base

# ORM 모델 클래스 정의
class Sales(Base):
    __tablename__ = 'sales'  # 테이블 이름
    
    id = Column(Integer, primary_key=True, index=True)
    sales_amount = Column(Float, nullable=False)  # 매출액
    month = Column(String(2), nullable=False)  # 월
