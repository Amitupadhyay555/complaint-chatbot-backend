# # from fastapi import FastAPI
# # from app.routers import chat, complaints
# # from app.database import engine
# # from app.models import Base

# # app = FastAPI(title="Complaint Chatbot API")

# # # Create database tables
# # Base.metadata.create_all(bind=engine)

# # # Include routers
# # app.include_router(chat.router, prefix="/chat", tags=["chat"])
# # app.include_router(complaints.router, prefix="/complaints", tags=["complaints"])



# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Optional
# import uuid
# from datetime import datetime
# from models import Base, Complaint as ComplaintModel
# from database import SessionLocal, engine
# from sqlalchemy.orm import Session
# import logging
# import os
# from pathlib import Path
# import re
# from utils import validate_email, validate_phone, extract_complaint_id

# # Initialize database
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Complaint Chatbot API")

# # CORS configuration
# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Simple RAG System without external dependencies
# class SimpleRAGSystem:
#     def __init__(self):
#         self.knowledge_base = self.load_knowledge_base()
    
#     def load_knowledge_base(self):
#         """Load knowledge base from file"""
#         try:
#             kb_path = "knowledge_base.txt"
#             if not os.path.exists(kb_path):
#                 # Create a default knowledge base if file doesn't exist
#                 default_kb = """
#                 Welcome to our customer service system. Here are some common issues and solutions:
                
#                 1. Password Reset: If you forgot your password, click on 'Forgot Password' on the login page.
#                 2. Account Issues: For account-related problems, please contact our support team.
#                 3. Technical Problems: Try clearing your browser cache and cookies.
#                 4. Billing Questions: Check your account dashboard for billing information.
#                 5. General Support: Our support team is available 24/7 to help you.
                
#                 For urgent issues, please call our helpline or email support@company.com
#                 """
#                 return default_kb
            
#             with open(kb_path, "r", encoding="utf-8") as f:
#                 return f.read()
#         except Exception as e:
#             logging.error(f"Error loading knowledge base: {str(e)}")
#             return "Default knowledge base loaded. Please contact support for assistance."
    
#     def query(self, question: str) -> str:
#         """Simple keyword-based search in knowledge base"""
#         question_lower = question.lower()
#         knowledge_lower = self.knowledge_base.lower()
        
#         # Simple keyword matching
#         keywords = ['password', 'account', 'technical', 'billing', 'support', 'login', 'help']
        
#         if any(keyword in question_lower for keyword in ['password', 'login', 'forgot']):
#             return "For password issues, please use the 'Forgot Password' feature on the login page or contact our support team."
#         elif any(keyword in question_lower for keyword in ['account', 'profile']):
#             return "For account-related issues, please check your account dashboard or contact our support team for assistance."
#         elif any(keyword in question_lower for keyword in ['technical', 'error', 'bug', 'problem']):
#             return "For technical issues, try clearing your browser cache and cookies. If the problem persists, please contact our technical support team."
#         elif any(keyword in question_lower for keyword in ['billing', 'payment', 'charge']):
#             return "For billing questions, please check your account dashboard for detailed billing information or contact our billing department."
#         else:
#             return "Thank you for your question. Our support team will get back to you shortly. For immediate assistance, please call our helpline or email support@company.com"

# # Initialize simple RAG system
# rag_system = SimpleRAGSystem()

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# class ComplaintCreate(BaseModel):
#     name: str
#     phone_number: str
#     email: str
#     complaint_details: str

# class ComplaintResponse(BaseModel):
#     complaint_id: str
#     name: str
#     phone_number: str
#     email: str
#     complaint_details: str
#     created_at: datetime

# class ChatMessage(BaseModel):
#     message: str
#     complaint_data: Optional[dict] = None

# # Helper function to extract information from message
# def extract_info_from_message(message: str, complaint_data: dict):
#     """Advanced extraction for name, phone, email, and complaint details using regex and NLP patterns"""
#     # Extract email
#     email_match = re.search(r'[\w\.-]+@[\w\.-]+', message)
#     if email_match:
#         complaint_data['email'] = email_match.group(0)
#     # Extract phone number
#     phone_match = re.search(r'(\+?\d[\d\- ]{8,}\d)', message)
#     if phone_match:
#         phone = phone_match.group(0).replace('-', '').replace(' ', '')
#         if validate_phone(phone):
#             complaint_data['phone_number'] = phone
#     # Extract name (look for 'my name is', 'I am', 'this is', or just a capitalized name)
#     name_match = re.search(r'(my name is|i am|this is)\s+([A-Za-z ]+)', message, re.IGNORECASE)
#     if name_match:
#         name = name_match.group(2).strip().split(',')[0]
#         complaint_data['name'] = name
#     elif not complaint_data.get('name') and len(message.split()) <= 5 and message.istitle():
#         complaint_data['name'] = message.strip()
#     # Extract complaint details (look for 'complaint details is', 'details:', or long text)
#     details_match = re.search(r'(complaint details is|details:|issue is|problem is)\s*(.+)', message, re.IGNORECASE)
#     if details_match:
#         complaint_data['complaint_details'] = details_match.group(2).strip()
#     elif (not any(x in message.lower() for x in ['name', 'phone', 'email'])) and len(message.split()) > 3:
#         complaint_data['complaint_details'] = message.strip()
#     return complaint_data

# @app.post("/complaints/", response_model=dict)
# def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
#     complaint_id = str(uuid.uuid4())
#     db_complaint = ComplaintModel(
#         complaint_id=complaint_id,
#         name=complaint.name,
#         phone_number=complaint.phone_number,
#         email=complaint.email,
#         complaint_details=complaint.complaint_details,
#         created_at=datetime.utcnow()
#     )
#     db.add(db_complaint)
#     db.commit()
#     db.refresh(db_complaint)
#     return {"complaint_id": complaint_id, "message": "Complaint created successfully"}

# @app.get("/complaints/{complaint_id}", response_model=ComplaintResponse)
# def get_complaint(complaint_id: str, db: Session = Depends(get_db)):
#     complaint = db.query(ComplaintModel).filter(ComplaintModel.complaint_id == complaint_id).first()
#     if not complaint:
#         raise HTTPException(status_code=404, detail="Complaint not found")
#     return complaint

# @app.post("/chat/", response_model=dict)
# async def chat_with_bot(chat_request: dict, db: Session = Depends(get_db)):
#     try:
#         message = chat_request.get("message", "")
#         complaint_data = chat_request.get("complaint_data", {
#             "name": None,
#             "phone_number": None,
#             "email": None,
#             "complaint_details": None
#         })
#         # 1. Check for complaint status queries
#         complaint_id = extract_complaint_id(message)
#         if complaint_id:
#             complaint = db.query(ComplaintModel).filter(ComplaintModel.complaint_id == complaint_id).first()
#             if complaint:
#                 return {"message": f"Complaint ID: {complaint.complaint_id}\nStatus: Registered\nName: {complaint.name}\nPhone: {complaint.phone_number}\nEmail: {complaint.email}\nDetails: {complaint.complaint_details}\nCreated At: {complaint.created_at}", "complaint_data": complaint_data}
#             else:
#                 return {"message": f"Sorry, I couldn't find a complaint with ID: {complaint_id}. Please check the ID and try again.", "complaint_data": complaint_data}
#         # 2. Extract info from message
#         complaint_data = extract_info_from_message(message, complaint_data)
#         # 3. Validate email/phone if present
#         if complaint_data.get("email") and not validate_email(complaint_data["email"]):
#             return {"message": "The email address provided seems invalid. Could you please provide a valid email address?", "complaint_data": complaint_data}
#         if complaint_data.get("phone_number") and not validate_phone(complaint_data["phone_number"]):
#             return {"message": "The phone number provided seems invalid. Could you please provide a valid phone number?", "complaint_data": complaint_data}
#         # 4. Check for missing fields
#         missing_fields = []
#         if not complaint_data.get("name"):
#             missing_fields.append("name")
#         if not complaint_data.get("phone_number"):
#             missing_fields.append("phone number")
#         if not complaint_data.get("email"):
#             missing_fields.append("email address")
#         if not complaint_data.get("complaint_details"):
#             missing_fields.append("complaint details")
#         # 5. FAQ/Knowledge base direct answer if not in complaint flow
#         faq_keywords = ["track my order", "return policy", "update my account", "contact customer support", "payment methods", "cancel my order", "faq", "help"]
#         if any(kw in message.lower() for kw in faq_keywords) and any(x in message.lower() for x in ['what', 'how', 'where', 'when', 'who', 'faq', 'policy', 'track', 'return', 'cancel', 'contact', 'payment']):
#             rag_response = rag_system.query(message)
#             return {"message": rag_response, "complaint_data": complaint_data}
#         # 6. Complaint creation triggers
#         complaint_trigger = any(
#             trigger in message.lower() for trigger in ["create complaint", "file complaint", "register complaint", "submit complaint"]
#         )
#         if complaint_trigger and not missing_fields:
#             return {"message": f"Thank you{', ' + complaint_data['name'] if complaint_data.get('name') else ''}! Your complaint is ready to be filed. Please confirm by saying 'create complaint'.", "complaint_data": complaint_data, "ready_to_create": True}
#         if complaint_trigger and missing_fields:
#             return {"message": f"To proceed, could you please provide the following: {', '.join(missing_fields)}?", "complaint_data": complaint_data}
#         # 7. If all fields are present, prompt to create complaint
#         if not missing_fields:
#             return {"message": f"Thank you{', ' + complaint_data['name'] if complaint_data.get('name') else ''}! I have all your information. Please say 'create complaint' to proceed.", "complaint_data": complaint_data}
#         # 8. If user is in complaint flow, prompt for missing fields
#         if missing_fields:
#             if len(missing_fields) == 1:
#                 bot_response = f"Thank you{', ' + complaint_data['name'] if complaint_data.get('name') else ''}. Could you please provide your {missing_fields[0]}?"
#             else:
#                 bot_response = f"Thank you{', ' + complaint_data['name'] if complaint_data.get('name') else ''}. Could you please provide your {', '.join(missing_fields[:-1])} and {missing_fields[-1]}?"
#             return {"message": bot_response, "complaint_data": complaint_data}
#         # 9. General fallback: RAG/FAQ
#         rag_response = rag_system.query(message)
#         bot_response = f"{rag_response}\n\nIf you'd like to file a complaint, please provide your name, phone number, email, and complaint details."
#         return {"message": bot_response, "complaint_data": complaint_data}
#     except Exception as e:
#         logging.error(f"Error in chat endpoint: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")

# @app.post("/create-complaint/", response_model=dict)
# async def create_complaint_from_chat(complaint_data: dict, db: Session = Depends(get_db)):
#     try:
#         # Validate we have all required fields
#         if not all([complaint_data.get("name"), 
#                    complaint_data.get("phone_number"), 
#                    complaint_data.get("email"), 
#                    complaint_data.get("complaint_details")]):
#             raise HTTPException(status_code=400, detail="Missing required fields")
        
#         # Create the complaint
#         complaint_id = str(uuid.uuid4())
#         db_complaint = ComplaintModel(
#             complaint_id=complaint_id,
#             name=complaint_data["name"],
#             phone_number=complaint_data["phone_number"],
#             email=complaint_data["email"],
#             complaint_details=complaint_data["complaint_details"],
#             created_at=datetime.utcnow()
#         )
#         db.add(db_complaint)
#         db.commit()
        
#         return {
#             "complaint_id": complaint_id,
#             "message": "Complaint created successfully! Your complaint ID is: " + complaint_id
#         }
#     except Exception as e:
#         db.rollback()
#         logging.error(f"Error creating complaint: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")

# @app.get("/search-knowledge/", response_model=dict)
# async def search_knowledge(query: str):
#     try:
#         response = rag_system.query(query)
#         return {"response": response}
#     except Exception as e:
#         logging.error(f"Error in knowledge search: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "message": "Complaint Chatbot API is running"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)




from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from models import Base, Complaint as ComplaintModel
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import logging
import os
from pathlib import Path
import re
from utils import validate_email, validate_phone, extract_complaint_id

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Complaint Chatbot API")

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple RAG System without external dependencies
class SimpleRAGSystem:
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load knowledge base from file"""
        try:
            kb_path = "knowledge_base.txt"
            if not os.path.exists(kb_path):
                # Create a default knowledge base if file doesn't exist
                default_kb = """
                Welcome to our customer service system. Here are some common issues and solutions:
                
                1. Password Reset: If you forgot your password, click on 'Forgot Password' on the login page.
                2. Account Issues: For account-related problems, please contact our support team.
                3. Technical Problems: Try clearing your browser cache and cookies.
                4. Billing Questions: Check your account dashboard for billing information.
                5. General Support: Our support team is available 24/7 to help you.
                
                For urgent issues, please call our helpline or email support@company.com
                """
                return default_kb
            
            with open(kb_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error loading knowledge base: {str(e)}")
            return "Default knowledge base loaded. Please contact support for assistance."
    
    def query(self, question: str) -> str:
        """Simple keyword-based search in knowledge base"""
        question_lower = question.lower()
        knowledge_lower = self.knowledge_base.lower()
        
        # Simple keyword matching
        keywords = ['password', 'account', 'technical', 'billing', 'support', 'login', 'help']
        
        if any(keyword in question_lower for keyword in ['password', 'login', 'forgot']):
            return "For password issues, please use the 'Forgot Password' feature on the login page or contact our support team."
        elif any(keyword in question_lower for keyword in ['account', 'profile']):
            return "For account-related issues, please check your account dashboard or contact our support team for assistance."
        elif any(keyword in question_lower for keyword in ['technical', 'error', 'bug', 'problem']):
            return "For technical issues, try clearing your browser cache and cookies. If the problem persists, please contact our technical support team."
        elif any(keyword in question_lower for keyword in ['billing', 'payment', 'charge']):
            return "For billing questions, please check your account dashboard for detailed billing information or contact our billing department."
        else:
            return "Thank you for your question. Our support team will get back to you shortly. For immediate assistance, please call our helpline or email support@company.com"

# Initialize simple RAG system
rag_system = SimpleRAGSystem()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ComplaintCreate(BaseModel):
    name: str
    phone_number: str
    email: str
    complaint_details: str

class ComplaintResponse(BaseModel):
    complaint_id: str
    name: str
    phone_number: str
    email: str
    complaint_details: str
    created_at: datetime

class ChatMessage(BaseModel):
    message: str
    complaint_data: Optional[dict] = None

# Helper function to extract information from message
def extract_info_from_message(message: str, complaint_data: dict):
    """Advanced extraction for name, phone, email, and complaint details using regex and NLP patterns"""
    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', message)
    if email_match:
        complaint_data['email'] = email_match.group(0)
    # Extract phone number
    phone_match = re.search(r'(\+?\d[\d\- ]{8,}\d)', message)
    if phone_match:
        phone = phone_match.group(0).replace('-', '').replace(' ', '')
        if validate_phone(phone):
            complaint_data['phone_number'] = phone
    # Extract name (look for 'my name is', 'I am', 'this is', or just a capitalized name)
    name_match = re.search(r'(my name is|i am|this is)\s+([A-Za-z ]+)', message, re.IGNORECASE)
    if name_match:
        name = name_match.group(2).strip().split(',')[0]
        complaint_data['name'] = name
    elif not complaint_data.get('name') and len(message.split()) <= 5 and message.istitle():
        complaint_data['name'] = message.strip()
    # Extract complaint details (look for 'complaint details is', 'details:', or long text)
    details_match = re.search(r'(complaint details is|details:|issue is|problem is)\s*(.+)', message, re.IGNORECASE)
    if details_match:
        complaint_data['complaint_details'] = details_match.group(2).strip()
    elif (not any(x in message.lower() for x in ['name', 'phone', 'email'])) and len(message.split()) > 3:
        complaint_data['complaint_details'] = message.strip()
    return complaint_data

# ROOT ENDPOINT - ADD THIS TO FIX 404 ERRORS
@app.get("/")
async def root():
    return {
        "message": "Welcome to Complaint Chatbot API",
        "version": "1.0.0",
        "status": "active",
        "description": "AI-powered complaint management system",
        "endpoints": {
            "health": "/health",
            "chat": "/chat/",
            "create_complaint": "/complaints/",
            "get_complaint": "/complaints/{complaint_id}",
            "create_complaint_from_chat": "/create-complaint/",
            "search_knowledge": "/search-knowledge/",
            "api_docs": "/docs",
            "redoc": "/redoc"
        },
        "usage": "Use /chat/ endpoint to interact with the chatbot for complaint filing"
    }

# FAVICON ENDPOINT - ADD THIS TO HANDLE FAVICON REQUESTS
@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}

@app.post("/complaints/", response_model=dict)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    complaint_id = str(uuid.uuid4())
    db_complaint = ComplaintModel(
        complaint_id=complaint_id,
        name=complaint.name,
        phone_number=complaint.phone_number,
        email=complaint.email,
        complaint_details=complaint.complaint_details,
        created_at=datetime.utcnow()
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return {"complaint_id": complaint_id, "message": "Complaint created successfully"}

@app.get("/complaints/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: str, db: Session = Depends(get_db)):
    complaint = db.query(ComplaintModel).filter(ComplaintModel.complaint_id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@app.post("/chat/", response_model=dict)
async def chat_with_bot(chat_request: dict, db: Session = Depends(get_db)):
    try:
        message = chat_request.get("message", "")
        complaint_data = chat_request.get("complaint_data", {
            "name": None,
            "phone_number": None,
            "email": None,
            "complaint_details": None
        })
        # 1. Check for complaint status queries
        complaint_id = extract_complaint_id(message)
        if complaint_id:
            complaint = db.query(ComplaintModel).filter(ComplaintModel.complaint_id == complaint_id).first()
            if complaint:
                return {"message": f"Complaint ID: {complaint.complaint_id}\nStatus: Registered\nName: {complaint.name}\nPhone: {complaint.phone_number}\nEmail: {complaint.email}\nDetails: {complaint.complaint_details}\nCreated At: {complaint.created_at}", "complaint_data": complaint_data}
            else:
                return {"message": f"Sorry, I couldn't find a complaint with ID: {complaint_id}. Please check the ID and try again.", "complaint_data": complaint_data}
        # 2. Extract info from message
        complaint_data = extract_info_from_message(message, complaint_data)
        # 3. Validate email/phone if present
        if complaint_data.get("email") and not validate_email(complaint_data["email"]):
            return {"message": "The email address provided seems invalid. Could you please provide a valid email address?", "complaint_data": complaint_data}
        if complaint_data.get("phone_number") and not validate_phone(complaint_data["phone_number"]):
            return {"message": "The phone number provided seems invalid. Could you please provide a valid phone number?", "complaint_data": complaint_data}
        # 4. Check for missing fields
        missing_fields = []
        if not complaint_data.get("name"):
            missing_fields.append("name")
        if not complaint_data.get("phone_number"):
            missing_fields.append("phone number")
        if not complaint_data.get("email"):
            missing_fields.append("email address")
        if not complaint_data.get("complaint_details"):
            missing_fields.append("complaint details")
        # 5. FAQ/Knowledge base direct answer if not in complaint flow
        faq_keywords = ["track my order", "return policy", "update my account", "contact customer support", "payment methods", "cancel my order", "faq", "help"]
        if any(kw in message.lower() for kw in faq_keywords) and any(x in message.lower() for x in ['what', 'how', 'where', 'when', 'who', 'faq', 'policy', 'track', 'return', 'cancel', 'contact', 'payment']):
            rag_response = rag_system.query(message)
            return {"message": rag_response, "complaint_data": complaint_data}
        # 6. Complaint creation triggers
        complaint_trigger = any(
            trigger in message.lower() for trigger in ["create complaint", "file complaint", "register complaint", "submit complaint"]
        )
        if complaint_trigger and not missing_fields:
            return {"message": f"Thank you{', ' + complaint_data['name'] if complaint_data.get('name') else ''}! Your complaint is ready to be filed. Please confirm by saying 'create complaint'.", "complaint_data": complaint_data, "ready_to_create": True}
        if complaint_trigger and missing_fields:
            return {"message": f"To proceed, could you please provide the following: {', '.join(missing_fields)}?", "complaint_data": complaint_data}
        # 7. If all fields are present, prompt to create complaint
        if not missing_fields:
            return {"message": f"Thank you{', ' + complaint_data['name'] if complaint_data.get('name') else ''}! I have all your information. Please say 'create complaint' to proceed.", "complaint_data": complaint_data}
        # 8. If user is in complaint flow, prompt for missing fields
        if missing_fields:
            if len(missing_fields) == 1:
                bot_response = f"Thank you{', ' + complaint_data['name'] if complaint_data.get('name') else ''}. Could you please provide your {missing_fields[0]}?"
            else:
                bot_response = f"Thank you{', ' + complaint_data['name'] if complaint_data.get('name') else ''}. Could you please provide your {', '.join(missing_fields[:-1])} and {missing_fields[-1]}?"
            return {"message": bot_response, "complaint_data": complaint_data}
        # 9. General fallback: RAG/FAQ
        rag_response = rag_system.query(message)
        bot_response = f"{rag_response}\n\nIf you'd like to file a complaint, please provide your name, phone number, email, and complaint details."
        return {"message": bot_response, "complaint_data": complaint_data}
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/create-complaint/", response_model=dict)
async def create_complaint_from_chat(complaint_data: dict, db: Session = Depends(get_db)):
    try:
        # Validate we have all required fields
        if not all([complaint_data.get("name"), 
                   complaint_data.get("phone_number"), 
                   complaint_data.get("email"), 
                   complaint_data.get("complaint_details")]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Create the complaint
        complaint_id = str(uuid.uuid4())
        db_complaint = ComplaintModel(
            complaint_id=complaint_id,
            name=complaint_data["name"],
            phone_number=complaint_data["phone_number"],
            email=complaint_data["email"],
            complaint_details=complaint_data["complaint_details"],
            created_at=datetime.utcnow()
        )
        db.add(db_complaint)
        db.commit()
        
        return {
            "complaint_id": complaint_id,
            "message": "Complaint created successfully! Your complaint ID is: " + complaint_id
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating complaint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/search-knowledge/", response_model=dict)
async def search_knowledge(query: str):
    try:
        response = rag_system.query(query)
        return {"response": response}
    except Exception as e:
        logging.error(f"Error in knowledge search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Complaint Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)