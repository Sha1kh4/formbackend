import os
from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, UploadFile, Form, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import SessionLocal, init_db, Invoice

app = FastAPI()


# Allow CORS (optional, useful for frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_FOLDER = Path("invoices")
UPLOAD_FOLDER.mkdir(exist_ok=True)

init_db()



# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Helper to check file type
def is_pdf(filename: str):
    return filename.lower().endswith(".pdf")


@app.post("/upload")
async def upload_invoice(
    clientname: str = Form(...),
    invoice: UploadFile = File(...),
    source: str = Form(...),
    db: Session = Depends(get_db)
):
    if not is_pdf(invoice.filename):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Save file with unique name
    file_ext = Path(invoice.filename).suffix
    unique_filename = f"{uuid4().hex}{file_ext}"
    file_path = UPLOAD_FOLDER / unique_filename

    with open(file_path, "wb") as f:
        f.write(await invoice.read())

    # Save metadata to DB
    new_invoice = Invoice(clientname=clientname,source=source, filename=unique_filename)
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return JSONResponse(
        content={"message": "Invoice uploaded successfully", "invoice_id": new_invoice.id},
        status_code=201
    )

@app.get("/invoices")
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    return [
        {
            "id": inv.id,
            "clientname": inv.clientname,
            "filename": inv.filename,
            "uploaded_at": inv.uploaded_at.isoformat(),
            "source": inv.source
        } for inv in invoices
    ]
