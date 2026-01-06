from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app import models

# Student CRUD operations
class StudentCRUD:
    @staticmethod
    def get_student(db: Session, student_id: int) -> Optional[models.Student]:
        return db.query(models.Student).filter(models.Student.id == student_id).first()
    
    @staticmethod
    def get_students(db: Session, skip: int = 0, limit: int = 100, 
                     search: Optional[str] = None) -> List[models.Student]:
        query = db.query(models.Student)
        
        if search:
            search_filter = or_(
                models.Student.first_name.ilike(f"%{search}%"),
                models.Student.last_name.ilike(f"%{search}%"),
                models.Student.email.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_students_count(db: Session, search: Optional[str] = None) -> int:
        query = db.query(models.Student)
        
        if search:
            search_filter = or_(
                models.Student.first_name.ilike(f"%{search}%"),
                models.Student.last_name.ilike(f"%{search}%"),
                models.Student.email.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.count()
    
    @staticmethod
    def create_student(db: Session, student_data: dict) -> models.Student:
        student = models.Student(**student_data)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    
    @staticmethod
    def update_student(db: Session, student_id: int, student_data: dict) -> Optional[models.Student]:
        student = StudentCRUD.get_student(db, student_id)
        if student:
            for key, value in student_data.items():
                if value is not None:
                    setattr(student, key, value)
            db.commit()
            db.refresh(student)
        return student
    
    @staticmethod
    def delete_student(db: Session, student_id: int) -> bool:
        student = StudentCRUD.get_student(db, student_id)
        if student:
            db.delete(student)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_students_by_group(db: Session, group_id: int) -> List[models.Student]:
        return db.query(models.Student).filter(models.Student.group_id == group_id).all()
    
    @staticmethod
    def add_student_to_group(db: Session, student_id: int, group_id: int) -> Optional[models.Student]:
        student = StudentCRUD.get_student(db, student_id)
        group = GroupCRUD.get_group(db, group_id)
        
        if student and group:
            student.group_id = group_id
            db.commit()
            db.refresh(student)
            return student
        return None
    
    @staticmethod
    def remove_student_from_group(db: Session, student_id: int) -> Optional[models.Student]:
        student = StudentCRUD.get_student(db, student_id)
        if student:
            student.group_id = None
            db.commit()
            db.refresh(student)
            return student
        return None
    
    @staticmethod
    def transfer_student(db: Session, student_id: int, new_group_id: int) -> Optional[models.Student]:
        student = StudentCRUD.get_student(db, student_id)
        new_group = GroupCRUD.get_group(db, new_group_id)
        
        if student and new_group:
            student.group_id = new_group_id
            db.commit()
            db.refresh(student)
            return student
        return None

# Group CRUD operations
class GroupCRUD:
    @staticmethod
    def get_group(db: Session, group_id: int) -> Optional[models.Group]:
        return db.query(models.Group).filter(models.Group.id == group_id).first()
    
    @staticmethod
    def get_groups(db: Session, skip: int = 0, limit: int = 100, 
                   search: Optional[str] = None) -> List[models.Group]:
        query = db.query(models.Group)
        
        if search:
            query = query.filter(models.Group.name.ilike(f"%{search}%"))
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_groups_count(db: Session, search: Optional[str] = None) -> int:
        query = db.query(models.Group)
        
        if search:
            query = query.filter(models.Group.name.ilike(f"%{search}%"))
        
        return query.count()
    
    @staticmethod
    def create_group(db: Session, group_data: dict) -> models.Group:
        group = models.Group(**group_data)
        db.add(group)
        db.commit()
        db.refresh(group)
        return group
    
    @staticmethod
    def update_group(db: Session, group_id: int, group_data: dict) -> Optional[models.Group]:
        group = GroupCRUD.get_group(db, group_id)
        if group:
            for key, value in group_data.items():
                if value is not None:
                    setattr(group, key, value)
            db.commit()
            db.refresh(group)
        return group
    
    @staticmethod
    def delete_group(db: Session, group_id: int) -> bool:
        group = GroupCRUD.get_group(db, group_id)
        if group:
            # Remove group association from students before deleting
            students = StudentCRUD.get_students_by_group(db, group_id)
            for student in students:
                student.group_id = None
            db.commit()
            
            db.delete(group)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_group_with_students(db: Session, group_id: int) -> Optional[models.Group]:
        return db.query(models.Group).filter(models.Group.id == group_id).first()