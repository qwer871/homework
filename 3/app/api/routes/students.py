from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app import schemas
from app.database import get_db
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        return StudentService.create_student(db, student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{student_id}", response_model=schemas.StudentWithGroupResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = StudentService.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/", response_model=schemas.StudentsList)
def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    result = StudentService.get_students(db, skip, limit, search)
    return {"students": result["students"], "total": result["total"]}

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated_student = StudentService.update_student(db, student_id, student)
        if not updated_student:
            raise HTTPException(status_code=404, detail="Student not found")
        return updated_student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    if not StudentService.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")

@router.post("/{student_id}/groups/{group_id}", response_model=schemas.StudentResponse)
def add_student_to_group(
    student_id: int,
    group_id: int,
    db: Session = Depends(get_db)
):
    student = StudentService.add_student_to_group(db, student_id, group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return student

@router.delete("/{student_id}/groups", response_model=schemas.StudentResponse)
def remove_student_from_group(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = StudentService.remove_student_from_group(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/groups/{group_id}", response_model=schemas.StudentsList)
def get_students_in_group(
    group_id: int,
    db: Session = Depends(get_db)
):
    students = StudentService.get_students_in_group(db, group_id)
    return {"students": students, "total": len(students)}

@router.put("/{student_id}/transfer/{new_group_id}", response_model=schemas.StudentResponse)
def transfer_student(
    student_id: int,
    new_group_id: int,
    db: Session = Depends(get_db)
):
    student = StudentService.transfer_student(db, student_id, new_group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return student