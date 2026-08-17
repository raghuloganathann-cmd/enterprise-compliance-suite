"""Core data models for the Enterprise Compliance Suite."""

from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    role: str = Field(default="viewer")  # admin | auditor | risk_manager | viewer
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Policy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: str
    version: str = Field(default="1.0")
    owner: str
    status: str = Field(default="draft")  # draft | active | retired
    effective_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ComplianceRequirement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    framework: str  # e.g. SOC 2, ISO 27001, GDPR, HIPAA
    reference_id: str  # e.g. CC6.1, Art. 30
    description: str
    status: str = Field(default="not_met")  # met | in_progress | not_met
    owner: str
    last_reviewed: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Audit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    audit_type: str = Field(default="internal")  # internal | external | regulatory
    status: str = Field(default="planned")  # planned | in_progress | completed
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    lead_auditor: Optional[str] = None
    findings_summary: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RiskItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: str = Field(default="Operational")
    severity: str = Field(default="medium")  # low | medium | high | critical
    likelihood: str = Field(default="medium")  # low | medium | high
    status: str = Field(default="open")  # open | mitigating | closed
    owner: str
    identified_date: date = Field(default_factory=date.today)
    notes: Optional[str] = None

    @property
    def severity_rank(self) -> int:
        return {"low": 1, "medium": 2, "high": 3, "critical": 4}.get(self.severity, 0)
