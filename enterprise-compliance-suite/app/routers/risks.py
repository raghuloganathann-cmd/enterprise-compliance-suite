from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import RiskItem

router = APIRouter(prefix="/api/risks", tags=["Risk Register"])


@router.get("/", response_model=List[RiskItem])
def list_risks(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(RiskItem)
    if status:
        query = query.where(RiskItem.status == status)
    if severity:
        query = query.where(RiskItem.severity == severity)
    return session.exec(query).all()


@router.get("/{risk_id}", response_model=RiskItem)
def get_risk(risk_id: int, session: Session = Depends(get_session)):
    risk = session.get(RiskItem, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    return risk


@router.post("/", response_model=RiskItem, status_code=201)
def create_risk(risk: RiskItem, session: Session = Depends(get_session)):
    risk.id = None
    session.add(risk)
    session.commit()
    session.refresh(risk)
    return risk


@router.put("/{risk_id}", response_model=RiskItem)
def update_risk(risk_id: int, updated: RiskItem, session: Session = Depends(get_session)):
    risk = session.get(RiskItem, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    data = updated.dict(exclude_unset=True, exclude={"id"})
    for key, value in data.items():
        setattr(risk, key, value)
    session.add(risk)
    session.commit()
    session.refresh(risk)
    return risk


@router.delete("/{risk_id}", status_code=204)
def delete_risk(risk_id: int, session: Session = Depends(get_session)):
    risk = session.get(RiskItem, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    session.delete(risk)
    session.commit()
