# Gọi thư viện FastAPI
from fastapi import FastAPI

# Tạo đối tượng app từ class FastAPI
app = FastAPI()

# Tạo decorator cho route gốc ("/")
@app.get("/")
def read_root():
    # Trả về một Dictionary (Python sẽ tự convert sang JSON)
    return {"message": "Chao mung ban den voi Ebook2LateX!"}