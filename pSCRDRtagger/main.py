import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, firestore, initialize_app

# Khởi tạo Firebase
cred = credentials.Certificate("đường/dẫn/tới/firebase-key.json")
initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class GiaoDich(BaseModel):
    user_id: str
    mo_ta: str
    so_tien: int

class NguoiDung(BaseModel):
    user_id: str
    ten: str
    email: str

@app.get("/")
def trang_chu():
    return {"message": "Chào mừng đến với trang chủ"}

@app.post("/giaodich")
def luu_giao_dich(giao_dich: GiaoDich):
    ref = db.collection('giaodich').add(giao_dich.dict())
    logging.info(f"Giao dịch đã lưu: {giao_dich.dict()}")
    return {"id": ref[1].id, "data": giao_dich.dict()}

@app.get("/nguoidung/{user_id}")
def xem_nguoi_dung(user_id: str):
    ref = db.collection('nguoidung').document(user_id).get()
    if ref.exists:
        return ref.to_dict()
    raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

@app.post("/nguoidung")
def dang_ky_nguoi_dung(nguoi_dung: NguoiDung):
    db.collection('nguoidung').document(nguoi_dung.user_id).set(nguoi_dung.dict())
    return {"message": "Người dùng đã được tạo thành công", "user_id": nguoi_dung.user_id}

@app.get("/giaodich/nguoidung/{user_id}")
def danh_sach_giao_dich_theo_nguoi_dung(user_id: str):
    giaodich = db.collection('giaodich').where('user_id', '==', user_id).stream()
    return [gd.to_dict() for gd in giaodich]

@app.get("/giaodich/chitiet/{giaodich_id}")
def chi_tiet_giao_dich(giaodich_id: str):
    ref = db.collection('giaodich').document(giaodich_id).get()
    if ref.exists:
        return ref.to_dict()
    raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
