# import os
# from datetime import datetime
# from typing import Dict, Any

# def get_current_timestamp() -> str:
#     return datetime.utcnow().isoformat()

# def format_response(content: str) -> Dict[str, Any]:
#     return {
#         "timestamp": get_current_timestamp(),
#         "content": content
#     }

# def validate_complaint_data(data: Dict[str, Any]) -> bool:
#     required_fields = ["title", "description"]
#     return all(field in data for field in required_fields)











import re
from datetime import datetime
from typing import Optional

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    # Basic phone number validation (10 digits)
    return phone.isdigit() and len(phone) >= 10

def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    if timestamp is None:
        timestamp = datetime.utcnow()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def extract_complaint_id(text: str):
    match = re.search(r'([a-f0-9\-]{36})', text)
    return match.group(1) if match else None