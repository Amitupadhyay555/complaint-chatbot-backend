from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ComplaintBase(BaseModel):
    title: str
    description: str

class ComplaintCreate(ComplaintBase):
    pass

class Complaint(ComplaintBase):
    id: int
    user_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResponseBase(BaseModel):
    content: str

class ResponseCreate(ResponseBase):
    pass

class Response(ResponseBase):
    id: int
    created_at: datetime
    complaint_id: int

    class Config:
        from_attributes = True
