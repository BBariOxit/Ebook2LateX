import os
import shutil
import uuid
from fastapi import FastAPI, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

app = FastAPI()

# 1. Tạo thư mục chứa PDF tự động nếu chưa có
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

# response_model chỉ định dữ liệu trả ra phải chui qua cái khuôn UserResponse
@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    # Lệnh SQLAlchemy để moi toàn bộ User từ DB
    users = db.query(models.User).all()
    return users

# 2. Endpoint Upload File Ăn Tiền
@app.post("/upload-pdf", response_model=schemas.DocumentResponse)
def upload_pdf(
    # Lấy user_id từ Form data vì mình chưa làm tính năng Login/Token
    user_id: uuid.UUID = Form(...), 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Bước lọc cặn: Đéo phải PDF thì cút
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Sai định dạng! Chỉ nhận file PDF.")

    # Tạo tên file độc nhất để chống ghi đè (thêm UUID vào trước tên file)
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Lưu file vật lý xuống ổ cứng (trong folder backend/uploads/)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file: {str(e)}")

    # Ghi thông tin file vào Database
    new_doc = models.Document(
        id=uuid.uuid4(),
        user_id=user_id,
        file_name=file.filename,
        file_path_url=f"/{file_path}",
        status="Uploaded" # Trạng thái ban đầu chờ AI xử lý
    )
    
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc