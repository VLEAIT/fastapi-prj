from fastapi import HTTPException,APIRouter,Depends,status
from sqlalchemy.orm import Session
from database import get_db
from models import Book,User
from schemas import BookCreate,BookResponse,BookUpdate
from typing import Annotated
from core import get_current_user


router=APIRouter(
    prefix="/books",
    tags=["books"]
)

DatabaseSession=Annotated[Session, Depends(get_db)]
CurrentUser=Annotated[User,Depends(get_current_User)]

def get_book_byid(db:DatabaseSession)->Book:
        book=db.query(Book).filter(Book.id==id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="data not found"
            )
        return book    

Target=Annotated[Book,Depends(get_book_byid)]   

@router.post("/",response_model=BookResponse,status_code=201)
def book_create(book:BookCreate,db:DatabaseSession,current_user:CurrentUser):
    db_book=Book(**book.model_dump(),owner_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/",response_model=list[BookResponse])
def get_bookall(db:DatabaseSession,point_skip:int=0,limit:int=10):
    return db.query(Book).offset(point_skip).limit(limit).all()
    

@router.get("/{id}",response_model=BookResponse)
def get_book(id:int,book:Target,db:DatabaseSession):
    return book
  

@router.put("/{id}",response_model=BookResponse)
def put_book(book:BookCreate,db:DatabaseSession,create_user:CurrentUser,db_book:Target):
    if db_book.owner_id!=create_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not authorized")
    for key,value in book.model_dump().items():
        setattr(db_book,key,value)
    db_book.owner_id=create_user.id    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.patch("/{id}",response_model=BookResponse)
def patch_book(book:BookUpdate,db:DatabaseSession,create_user:CurrentUser,db_book:Target):
    if db_book.owner_id!=create_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not authorized")
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book,key,value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(db:DatabaseSession,current_user:CurrentUser,db_book:target):
    if db_book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=" user is not authroried")
    db.delete(db_book)
    db.commit()
    return None       


    



        
        
    








         


