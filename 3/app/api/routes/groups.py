from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app import schemas
from app.database import get_db
from app.services.group_service import GroupService

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=schemas.GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(
    group: schemas.GroupCreate,
    db: Session = Depends(get_db)
):
    try:
        return GroupService.create_group(db, group)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{group_id}", response_model=schemas.GroupResponse)
def get_group(
    group_id: int,
    db: Session = Depends(get_db)
):
    group = GroupService.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.get("/", response_model=schemas.GroupsList)
def get_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    result = GroupService.get_groups(db, skip, limit, search)
    return {"groups": result["groups"], "total": result["total"]}

@router.put("/{group_id}", response_model=schemas.GroupResponse)
def update_group(
    group_id: int,
    group: schemas.GroupUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated_group = GroupService.update_group(db, group_id, group)
        if not updated_group:
            raise HTTPException(status_code=404, detail="Group not found")
        return updated_group
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    group_id: int,
    db: Session = Depends(get_db)
):
    if not GroupService.delete_group(db, group_id):
        raise HTTPException(status_code=404, detail="Group not found")