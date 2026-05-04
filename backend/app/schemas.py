from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Khuôn này dùng để xuất dữ liệu trả về cho Frontend (Response)
class UserResponse(BaseModel):
    user_id: UUID
    username_email: str
    full_name: str
    role: str
    is_active: bool
    created_at: Optional[datetime] = None
    
    # LƯU Ý: Tuyệt đối ko cho trường password_hash vào đây nhé!
    
    # Bật chế độ tự động map với SQLAlchemy ORM
    class Config:
        from_attributes = True