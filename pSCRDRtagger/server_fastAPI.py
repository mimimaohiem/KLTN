import data_processing

from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, firestore, initialize_app
from typing import List
from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

from text_processing import process_text # type: ignore
from pos_tagger import pos_tag # type: ignore


app = FastAPI()

# Thiết lập Firebase
cred = credentials.Certificate("path/to/your-firebase-adminsdk.json")
initialize_app(cred)
db = firestore.client()
financial_records = db.collection('financial_records')

# Mô hình dữ liệu cho các record
class FinancialRecord(BaseModel):
    user_id: str
    description: str
    amount: float

# Mô hình dữ liệu cho đăng ký người dùng
class User(BaseModel):
    user_id: str
    name: str

# API để lưu thông tin thu chi vào Firebase
@app.post("/record/")
async def create_record(record: FinancialRecord):
    doc_ref = financial_records.document()
    doc_ref.set(record.dict())
    return {"msg": "Record saved", "data": record.dict()}

# API để đăng ký người dùng mới
@app.post("/register/")
async def register_user(user: User):
    user_ref = db.collection('users').document(user.user_id)
    user_ref.set(user.dict())
    return {"msg": "User registered", "user_id": user.user_id}

# API để liệt kê danh sách thu chi theo từng người dùng
@app.get("/records/{user_id}/")
async def list_records(user_id: str):
    records = financial_records.where('user_id', '==', user_id).stream()
    return [doc.to_dict() for doc in records]

# API để hiển thị chi tiết của một item thu chi
@app.get("/record/{doc_id}/")
async def get_record(doc_id: str):
    doc = financial_records.document(doc_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Record not found")
