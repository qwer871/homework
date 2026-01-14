from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app import schemas, crud
from app.models import Group

class GroupService:
    @staticmethod
    def create_group(db: Session, group_in: schemas.GroupCreate) -> Group:
        # Check if group name already exists
        existing_group = db.query(Group).filter(Group.name == group_in.name).first()
        if existing_group:
            raise ValueError(f"Group with name {group_in.name} already exists")
        
        group_data = group_in.model_dump()
        return crud.GroupCRUD.create_group(db, group_data)
    
    @staticmethod
    def get_group(db: Session, group_id: int) -> Optional[Group]:
        return crud.GroupCRUD.get_group_with_students(db, group_id)
    
    @staticmethod
    def get_groups(db: Session, skip: int = 0, limit: int = 100, 
                   search: Optional[str] = None) -> Dict[str, Any]:
        groups = crud.GroupCRUD.get_groups(db, skip, limit, search)
        total = crud.GroupCRUD.get_groups_count(db, search)
        
        return {
            "groups": groups,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
    @staticmethod
    def update_group(db: Session, group_id: int, 
                     group_in: schemas.GroupUpdate) -> Optional[Group]:
        # Check if group exists
        group = crud.GroupCRUD.get_group(db, group_id)
        if not group:
            return None
        
        # Check if new name conflicts with existing group
        if group_in.name and group_in.name != group.name:
            existing_group = db.query(Group).filter(
                Group.name == group_in.name,
                Group.id != group_id
            ).first()
            if existing_group:
                raise ValueError(f"Group with name {group_in.name} already exists")
        
        update_data = group_in.model_dump(exclude_unset=True)
        return crud.GroupCRUD.update_group(db, group_id, update_data)
    
    @staticmethod
    def delete_group(db: Session, group_id: int) -> bool:
        return crud.GroupCRUD.delete_group(db, group_id)