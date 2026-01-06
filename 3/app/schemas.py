from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Base schemas
class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=120)
    group_id: Optional[int] = None

class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

# Create schemas
class StudentCreate(StudentBase):
    pass

class GroupCreate(GroupBase):
    pass

# Update schemas
class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    group_id: Optional[int] = None

class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

# Response schemas
class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class GroupResponse(GroupBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    students: List[StudentResponse] = []
    
    class Config:
        from_attributes = True

class StudentWithGroupResponse(StudentResponse):
    group: Optional[GroupResponse] = None

# List schemas
class StudentsList(BaseModel):
    students: List[StudentResponse]
    total: int

class GroupsList(BaseModel):
    groups: List[GroupResponse]
    total: int

# Transfer schema
class StudentTransfer(BaseModel):
    student_id: int
    from_group_id: int
    to_group_id: int