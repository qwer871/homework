from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app import schemas, crud
from app.models import Student

class StudentService:
    @staticmethod
    def create_student(db: Session, student_in: schemas.StudentCreate) -> Student:
        # Check if email already exists
        existing_student = db.query(Student).filter(Student.email == student_in.email).first()
        if existing_student:
            raise ValueError(f"Student with email {student_in.email} already exists")
        
        student_data = student_in.model_dump()
        return crud.StudentCRUD.create_student(db, student_data)
    
    @staticmethod
    def get_student(db: Session, student_id: int) -> Optional[Student]:
        return crud.StudentCRUD.get_student(db, student_id)
    
    @staticmethod
    def get_students(db: Session, skip: int = 0, limit: int = 100, 
                     search: Optional[str] = None) -> Dict[str, Any]:
        students = crud.StudentCRUD.get_students(db, skip, limit, search)
        total = crud.StudentCRUD.get_students_count(db, search)
        
        return {
            "students": students,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
    @staticmethod
    def update_student(db: Session, student_id: int, 
                       student_in: schemas.StudentUpdate) -> Optional[Student]:
        # Check if student exists
        student = crud.StudentCRUD.get_student(db, student_id)
        if not student:
            return None
        
        # Check if new email conflicts with existing student
        if student_in.email and student_in.email != student.email:
            existing_student = db.query(Student).filter(
                Student.email == student_in.email,
                Student.id != student_id
            ).first()
            if existing_student:
                raise ValueError(f"Student with email {student_in.email} already exists")
        
        update_data = student_in.model_dump(exclude_unset=True)
        return crud.StudentCRUD.update_student(db, student_id, update_data)
    
    @staticmethod
    def delete_student(db: Session, student_id: int) -> bool:
        return crud.StudentCRUD.delete_student(db, student_id)
    
    @staticmethod
    def add_student_to_group(db: Session, student_id: int, group_id: int) -> Optional[Student]:
        return crud.StudentCRUD.add_student_to_group(db, student_id, group_id)
    
    @staticmethod
    def remove_student_from_group(db: Session, student_id: int) -> Optional[Student]:
        return crud.StudentCRUD.remove_student_from_group(db, student_id)
    
    @staticmethod
    def transfer_student(db: Session, student_id: int, new_group_id: int) -> Optional[Student]:
        return crud.StudentCRUD.transfer_student(db, student_id, new_group_id)
    
    @staticmethod
    def get_students_in_group(db: Session, group_id: int) -> List[Student]:
        return crud.StudentCRUD.get_students_by_group(db, group_id)