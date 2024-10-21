from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 URL (또는 다른 DB URL로 변경)
DATABASE_URL = "sqlite:///./sales.db"

# 데이터베이스 연결 및 세션 설정
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 정의
Base = declarative_base()

# 테이블 생성 (Sales와 Todo 테이블이 sales.db에 생성됨)
Base.metadata.create_all(bind=engine)
