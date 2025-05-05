from typing import Optional, List, Dict, Any,Union
from pydantic import BaseModel, Field, EmailStr, constr,validator
from datetime import datetime
from enum import Enum

import re

class BooksIn(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    quantity: int = Field(gt=0)
    available: int = Field(gt=0)




class BooksOut(BooksIn):
    created_at: datetime
    id: int

    class Config:
        from_attributes = True



class MembersIn(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    middle_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    gender: str = Field(min_length=3, max_length=7)
    phone: constr(min_length=10, max_length=15, pattern=r'^\+?[1-9]\d{9,14}$')

class MembersOut(MembersIn):
    created_at: datetime
    id: int

    class Config:
        from_attributes = True


class BorrowedIn(BaseModel):
    member_id: int = Field(gt=0)
    book_id: int = Field(gt=0)
    returned_at: Optional[datetime] = None
    expected_at: Optional[datetime]= None
    


class BorrowedOut(BorrowedIn):
    id: int
    issued_at: datetime
    
    status: str 
    fine: Optional[int] = None
    borrower: MembersOut
    books_borrowed: BooksOut
    # fine: Optional[int] = Field(ge=0)

    class Config:
        from_attributes = True 
