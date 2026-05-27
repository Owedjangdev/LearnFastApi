from fastapi import FastAPI, Depends
from database import get_db, engine
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel

app = FastAPI()

class UpdateBook(BaseModel):
    title: str
    author: str
    publish_date: str

class Bookstore(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str

@app.post("/books")
def create_book(book: Bookstore, db: Session = Depends(get_db)):
    new_book = model.Book(id=book.id, title=book.title, author=book.author, publish_date=book.publish_date)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/")
def read_books(db: Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books

@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if book is None:
        return {"message": "Book not found"}
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: UpdateBook, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if book is None:
        return {"message": "Book not found"}
    book.title = updated_book.title
    book.author = updated_book.author
    book.publish_date = updated_book.publish_date
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if book is None:
        return {"message": "Book not found"}
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}