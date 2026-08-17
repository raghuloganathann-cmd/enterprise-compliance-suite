from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Policy

router = APIRouter(prefix="/api/policies", tags=["Policies"])


@router.get("/", response_model=List[Policy])
def list_policies(
    status: Optional[str] = None,
    category: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(Policy)
    if status:
        query = query.where(Policy.status == status)
    if category:
        query = query.where(Policy.category == category)
    return session.exec(query).all()


@router.get("/{policy_id}", response_model=Policy)
def get_policy(policy_id: int, session: Session = Depends(get_session)):
    policy = session.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.post("/", response_model=Policy, status_code=201)
def create_policy(policy: Policy, session: Session = Depends(get_session)):
    policy.id = None
    session.add(policy)
    session.commit()
    session.refresh(policy)
    return policy


@router.put("/{policy_id}", response_model=Policy)
def update_policy(policy_id: int, updated: Policy, session: Session = Depends(get_session)):
    policy = session.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    data = updated.dict(exclude_unset=True, exclude={"id"})
    for key, value in data.items():
        setattr(policy, key, value)
    session.add(policy)
    session.commit()
    session.refresh(policy)
    return policy


@router.delete("/{policy_id}", status_code=204)
def delete_policy(policy_id: int, session: Session = Depends(get_session)):
    policy = session.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    session.delete(policy)
    session.commit()
