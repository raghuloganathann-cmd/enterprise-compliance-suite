from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Audit

router = APIRouter(prefix="/api/audits", tags=["Audits"])


@router.get("/", response_model=List[Audit])
def list_audits(
    status: Optional[str] = None,
    audit_type: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(Audit)
    if status:
        query = query.where(Audit.status == status)
    if audit_type:
        query = query.where(Audit.audit_type == audit_type)
    return session.exec(query).all()


@router.get("/{audit_id}", response_model=Audit)
def get_audit(audit_id: int, session: Session = Depends(get_session)):
    audit = session.get(Audit, audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit


@router.post("/", response_model=Audit, status_code=201)
def create_audit(audit: Audit, session: Session = Depends(get_session)):
    audit.id = None
    session.add(audit)
    session.commit()
    session.refresh(audit)
    return audit


@router.put("/{audit_id}", response_model=Audit)
def update_audit(audit_id: int, updated: Audit, session: Session = Depends(get_session)):
    audit = session.get(Audit, audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    data = updated.dict(exclude_unset=True, exclude={"id"})
    for key, value in data.items():
        setattr(audit, key, value)
    session.add(audit)
    session.commit()
    session.refresh(audit)
    return audit


@router.delete("/{audit_id}", status_code=204)
def delete_audit(audit_id: int, session: Session = Depends(get_session)):
    audit = session.get(Audit, audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    session.delete(audit)
    session.commit()
