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



class Members(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    middle_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: constr(min_length=10, max_length=15, pattern=r'^\+?[1-9]\d{9,14}$')

class MembersIn(Members):
    created_at: datetime
class MembersOut(Members):
    id: int

    class Config:
        orm_mode = True


class Borrowed(BaseModel):
    member_id: int = Field(gt=0)
    book_id: int = Field(gt=0)
    issued_at: datetime
    expected_at: datetime
    returned_at: Optional[datetime] = None
    fine: Optional[int] = Field(ge=0)

class BorrowedIn(Borrowed):
    pass
class BorrowedOut(Borrowed):
    id: int

    class Config:
        orm_mode = True 