# from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# class Complaint(Base):
#     __tablename__ = "complaints"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String, index=True)
#     title = Column(String)
#     description = Column(Text)
#     status = Column(String, default="pending")
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     responses = relationship("Response", back_populates="complaint")

# class Response(Base):
#     __tablename__ = "responses"

#     id = Column(Integer, primary_key=True, index=True)
#     complaint_id = Column(Integer, ForeignKey("complaints.id"))
#     content = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     complaint = relationship("Complaint", back_populates="responses")





from sqlalchemy import Column, String, DateTime, Text
from database import Base
from datetime import datetime

class Complaint(Base):
    __tablename__ = "complaints"
    
    complaint_id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    complaint_details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)