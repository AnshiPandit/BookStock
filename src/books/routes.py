from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.books.models import Book
from src.db.main import get_session
from uuid import UUID
from typing import List

# APIRouter instance
book_router = APIRouter()

book_service = BookService()

# response_model is used in FastAPI to define the structure of the response that your API should return. It ensures that the output follows a specific format.
@book_router.get('/', response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books

# status module provides all status codes
@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data:BookCreateModel, session:AsyncSession = Depends(get_session)) -> dict:
    # model_dump allows to use book_data as a dicitonary
    new_book = await book_service.create_book(book_data, session)
    return new_book

# path parameter
@book_router.get('/{book_uid}')
async def get_book(book_uid:UUID, session:AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return
    else:
        # FastAPI you throw exception using HTTPException class
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Book not found")

@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(book_uid:UUID,book_update_data:BookUpdateModel, session:AsyncSession = Depends(get_session)) -> dict:
    
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    
    # handling cases where book is not found
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# nothing to return 
@book_router.delete('/{book_uid}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid:UUID, session:AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    
    if not book_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return {}