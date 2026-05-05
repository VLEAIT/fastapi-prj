from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from schemas import BookCreate,BookResponse,BookUpdate


router=APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/",response_model=BookResponse,status_code=201)
def book_create(book:BookCreate,db:Session=Depends(get_db)):
    db_book=Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/",response_model=list[BookResponse])
def get_bookall(point_skip:int=0,limit:int=10,db:Session=Depends(get_db)):
    return db.query(Book).offset(point_skip).limit(limit).all()
    

@router.get("/{id}",response_model=BookResponse)
def get_book(id:int,db:Session=Depends(get_db)):
    book=db.query(Book).filter(Book.id==id).first()
    if book  not in Book:
        raise HTTPSExtension(status_code=404,detail="Book Not Found") 
    return book

@router.put("/{id}",reponse_model=BookResponse)
def put_book(id:int,book:BookCreate,db:Session=Depends(get_db)):
    db_book=db.query(Book).filter(Book.id==id).first()
    if not db_book:
        HTTPSExtension(status_code=404,detail="Book not found")

    for key,value in book.model_dump().items():
        setattr(db_book,key,value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.patch("/{id}",response_model=BookResponse)
def patch_book(id:int,book:BookUpdate,db:Session=Depends(get_db)):
    db_book=db.query(Book).filter(Book.id==id).first()
    if not db_book:
        raise HTTPException(status_code=404,detail="Book not found")
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book,key,value)
    db.commit()
    db.refresh(db_book)
    return(db_book)

@router.delete("/{id}",status_code=204)
def delete_db(id:int,db:Session=Depends(get_db)):
    db_book=db.query(Book).filter(Book.id==id).first()
    if not db_book:
        HTTPSException(status_code=404,detail="Book not found")
    db.delete(db_book)
    db.commit()
    return None



        
        
    








         


