from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

app = FastAPI()

# Hàm này là cái "Ống hút": Mỗi khi có Request, nó mở 1 Session DB
# Xử lý xong request nó tự động chui vào 'finally' để đóng Session lại. Cực an toàn!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Giữ lại cái Hello World cho đỡ trống trải
@app.get("/")
def read_root():
    return {"message": "Chao mung ban den voi Ebook2LateX!"}

# ĐÂY LÀ ENDPOINT ĂN TIỀN CỦA MÀY NÀY!
# response_model chỉ định dữ liệu trả ra phải chui qua cái khuôn UserResponse
@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    # Lệnh SQLAlchemy để moi toàn bộ User từ DB
    users = db.query(models.User).all()
    return users