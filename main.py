import os
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, UploadFile, Form, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import SessionLocal, init_db, Invoice

app = FastAPI()

# Enable CORS for all (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload folders exist
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

RECEIPT_FOLDER = UPLOAD_FOLDER / "receipts"
RECEIPT_FOLDER.mkdir(exist_ok=True)

INVOICE_FOLDER = UPLOAD_FOLDER / "invoices"
INVOICE_FOLDER.mkdir(exist_ok=True)

init_db()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def allowed_file(filename: str, allowed_exts):
    ext = Path(filename).suffix.lower()
    return ext in allowed_exts

@app.post("/income")
async def create_income(
    name: str = Form(...),
    amount: float = Form(...),
    date: str = Form(...),
    source: str = Form(...),
    notes: str = Form(""),
    invoice: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    filename = None
    if invoice:
        if not allowed_file(invoice.filename, {".pdf", ".jpg", ".jpeg", ".png"}):
            raise HTTPException(status_code=400, detail="Invalid file type for invoice. Allowed: PDF, JPG, PNG")
        ext = Path(invoice.filename).suffix
        filename = f"{uuid4().hex}{ext}"
        file_path = INVOICE_FOLDER / filename
        with open(file_path, "wb") as f:
            f.write(await invoice.read())

    new_invoice = Invoice(
        name=name,
        amount=amount,
        date=date,
        type="income",
        source_or_category=source,
        payment_method=None,
        notes=notes,
        filename=filename
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return JSONResponse(content={"message": "Income saved successfully", "id": new_invoice.id}, status_code=201)


@app.post("/expenses")
async def create_expense(
    name: str = Form(...),
    amount: float = Form(...),
    date: str = Form(...),
    category: str = Form(...),
    payment: str = Form(...),
    notes: str = Form(""),
    receipt: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    filename = None
    if receipt:
        if not allowed_file(receipt.filename, {".pdf", ".jpg", ".jpeg", ".png"}):
            raise HTTPException(status_code=400, detail="Invalid file type for receipt. Allowed: PDF, JPG, PNG")
        ext = Path(receipt.filename).suffix
        filename = f"{uuid4().hex}{ext}"
        file_path = RECEIPT_FOLDER / filename
        with open(file_path, "wb") as f:
            f.write(await receipt.read())

    new_expense = Invoice(
        name=name,
        amount=amount,
        date=date,
        type="expense",
        source_or_category=category,
        payment_method=payment,
        notes=notes,
        filename=filename
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return JSONResponse(content={"message": "Expense saved successfully", "id": new_expense.id}, status_code=201)

@app.get("/invoices")
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).order_by(Invoice.uploaded_at.desc()).all()
    return [
        {
            "id": i.id,
            "name": i.name,
            "amount": i.amount,
            "type": i.type,
            "date": i.date,
            "source_or_category": i.source_or_category,
            "payment_method": i.payment_method,
            "notes": i.notes,
            "filename": i.filename,
            "uploaded_at": i.uploaded_at.isoformat()
        }
        for i in invoices
    ]

@app.get("/")
def root():
    return {"message": "Welcome to the Invoice API"}
