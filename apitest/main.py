from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

books_db = [{"id": 1, "title": "Python", "author": "idk lol"}, {"id": 2, "title": "C++", "author": "nikita"}]


class BookSchema(BaseModel):
    title: str
    author: str


@app.get("/books")
def get_books():
    return books_db


@app.post("/books")
def add_book(book: BookSchema):
    new_book_id = len(books_db) + 1
    books_db.append({"id": new_book_id, "title": book.title, "author": book.author})
    return {"ok": True}


@app.put("/books/{book_id}")
def put_book(book_id: int, data: BookSchema):
    books_db[book_id - 1] = {"id": book_id, "title": data.title, "author": data.author}
    return {"ok": True}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    del books_db[book_id]
    return {"ok": True}
