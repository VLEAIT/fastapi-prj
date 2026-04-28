from fastapi import FastAPI,HTTPSException
from pydantic import BaseModel,Field
from typing import Optional

app=FastAPI()

class BookCreate(BaseModel):
    title:str=Field(min_length=1,max_length=100)
    author:str
    pages:int=Field(gt=0)
    price:int=Field(ge=0)   
    description:Optional[str]=None

class BookResponse(BookCreate):
    id:   
    model_config={"from_attributes":True}

class BookUpdate(BaseModel):
    title:Optional[str]=None
    author:Optional[str]=None
    pages:Optional[int]=None
    price:Optional[float]=None


books:dict[int,dict]={}
counter=1

@app.post('/books',response_model=BookResponse,status_code=201)
async def create_book(book:BookCreate):
    global counter
    new_book={"id":counter,**book.model_dump()}
    books[counter]=new_book
    counter+=1
    return new_book

@app.get("/books"/{id},response_model=BookResponse,status_code=200)
async def get_book(id:int):
    if id not in books:
        raise HTTPException(status_code=404,detail="book not found")
    return books[id]

@app.put("/books/{id}",response_model=BookResponse)
async def replace_book(id:int,book:BookCreate):
    books[id]:{"id":id,**book.model_dump()}
    return books[id]

@app.patch('/books/{id}',response_model=BookResponse)
async def patial_update(id:int,book:BookUpdate):
    stored=books[id]
    updates=book.model_dump(exclude_unset=True)
    stored.update(updates)
    return stored

@app.delete('/books{id}',status_code=204)
async def delete_book(id:int):
    del books[id]
