from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal
from auth import authenticate_user, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 TOKEN ENDPOINT (OAuth2)
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": user["username"], "token_type": "bearer"}

# 📘 READ BOOKS (Protected)
@app.get("/")
def read_books(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return db.query(models.Books).all()

# ➕ CREATE BOOK (Protected)
@app.post("/")
def create_book(
    book: schemas.Book,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    book_model = models.Books(**book.dict())
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model
