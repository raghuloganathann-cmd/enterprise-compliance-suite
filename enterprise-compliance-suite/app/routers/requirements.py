from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import ComplianceRequirement

router = APIRouter(prefix="/api/requirements", tags=["Compliance Requirements"])


@router.get("/", response_model=List[ComplianceRequirement])
def list_requirements(
    framework: Optional[str] = None,
    status: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(ComplianceRequirement)
    if framework:
        query = query.where(ComplianceRequirement.framework == framework)
    if status:
        query = query.where(ComplianceRequirement.status == status)
    return session.exec(query).all()


@router.get("/{req_id}", response_model=ComplianceRequirement)
def get_requirement(req_id: int, session: Session = Depends(get_session)):
    req = session.get(ComplianceRequirement, req_id)
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return req


@router.post("/", response_model=ComplianceRequirement, status_code=201)
def create_requirement(req: ComplianceRequirement, session: Session = Depends(get_session)):
    req.id = None
    session.add(req)
    session.commit()
    session.refresh(req)
    return req


@router.put("/{req_id}", response_model=ComplianceRequirement)
def update_requirement(req_id: int, updated: ComplianceRequirement, session: Session = Depends(get_session)):
    req = session.get(ComplianceRequirement, req_id)
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    data = updated.dict(exclude_unset=True, exclude={"id"})
    for key, value in data.items():
        setattr(req, key, value)
    session.add(req)
    session.commit()
    session.refresh(req)
    return req


@router.delete("/{req_id}", status_code=204)
def delete_requirement(req_id: int, session: Session = Depends(get_session)):
    req = session.get(ComplianceRequirement, req_id)
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    session.delete(req)
    session.commit()
