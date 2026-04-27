from fastapi import FastAPI
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
    id:int
    model_config={"from_attributes":True}

books:dict[int,dict]={}
counter=1

@app.post('/books',response_model=BookResponse,status_code=201)
async def create_book(book:BookCreate):
    global counter
    new_book={"id":counter,**book.model_dump()}
    books[counter]=new_book
    counter+=1
    return new_book
