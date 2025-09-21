from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional



app = FastAPI(title="Library API", description="API for managing a library")

#  definning model for books
class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    year: int
    pages: int
    is_available: bool = True

# defining model for updating books
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    pages: Optional[int] = None
    is_available: Optional[bool] = None


# a list for a temporary database
book_db = []
next_id = 1
def get_next_id():
    global next_id
    current_id = next_id
    next_id += 1  
    return current_id



# Get all books
@app.get("/books", response_model=List[Book])
def get_all_books():
    return book_db

# GET a book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in book_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# POST a new book
@app.post("/books", response_model=Book)
def create_book(book: Book):
    book.id = get_next_id()  # creating a new ID
    book_db.append(book.model_dump())
    return book


# Update a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate):
    for i, book in enumerate(book_db):
        if book["id"] == book_id:
            update_data = book_update.model_dump(exclude_unset=True)
            book_db[i].update(update_data)
            return book_db[i]
    raise HTTPException(status_code=404, detail="Book not found")


# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(book_db):
        if book["id"] == book_id:
            deleted_book = book_db.pop(i)
            return {"message": f"Book {deleted_book["title"]} deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


# Search for books
@app.get("/books/search/", response_model=List[Book])
def search_books(author: Optional[str] = None, year: Optional[str] = None):
    result = book_db

    if author:
        result = [book for book in result if author.lower() in book["author"].lower()]

    if year:
        result = [book for book in result if book["year"] == year]

    return result


# endpoint for checking the status of next_id and current ids
@app.get("/status")
def get_status():
    return {
        "total_books": len(book_db),
        "next_id": next_id,
        "book_ids": [book["id"] for book in book_db]
    }

