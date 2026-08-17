"""Database engine and session management (SQLite by default)."""

from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./compliance_suite.db"

# check_same_thread=False needed for SQLite + FastAPI's threaded requests
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Create all tables if they don't exist, then seed demo data if empty."""
    SQLModel.metadata.create_all(engine)
    _seed_if_empty()


def get_session():
    """FastAPI dependency that yields a DB session."""
    with Session(engine) as session:
        yield session


def _seed_if_empty() -> None:
    from app.models import User, Policy, ComplianceRequirement, Audit, RiskItem
    from datetime import date, timedelta

    with Session(engine) as session:
        existing = session.exec(User.__table__.select()).first() if False else None
        from sqlmodel import select
        if session.exec(select(User)).first():
            return  # already seeded

        admin = User(name="Alex Admin", email="admin@example.com", role="admin")
        auditor = User(name="Jamie Auditor", email="auditor@example.com", role="auditor")
        session.add(admin)
        session.add(auditor)

        p1 = Policy(
            title="Data Protection & Privacy Policy",
            category="Data Privacy",
            version="2.1",
            owner="Legal & Compliance",
            status="active",
            effective_date=date.today() - timedelta(days=120),
        )
        p2 = Policy(
            title="Access Control Policy",
            category="Information Security",
            version="1.4",
            owner="IT Security",
            status="active",
            effective_date=date.today() - timedelta(days=45),
        )
        session.add(p1)
        session.add(p2)

        r1 = ComplianceRequirement(
            framework="SOC 2",
            reference_id="CC6.1",
            description="Logical access controls restrict access to authorized users.",
            status="met",
            owner="IT Security",
        )
        r2 = ComplianceRequirement(
            framework="GDPR",
            reference_id="Art. 30",
            description="Maintain records of processing activities.",
            status="in_progress",
            owner="Legal & Compliance",
        )
        r3 = ComplianceRequirement(
            framework="ISO 27001",
            reference_id="A.5.1",
            description="Policies for information security shall be defined and approved.",
            status="not_met",
            owner="CISO",
        )
        session.add(r1)
        session.add(r2)
        session.add(r3)

        a1 = Audit(
            name="Q3 Internal Security Audit",
            audit_type="internal",
            status="in_progress",
            scheduled_date=date.today() + timedelta(days=10),
            lead_auditor="Jamie Auditor",
        )
        session.add(a1)

        risk1 = RiskItem(
            title="Unpatched servers in staging environment",
            category="Technical",
            severity="high",
            likelihood="medium",
            status="open",
            owner="IT Security",
        )
        risk2 = RiskItem(
            title="Vendor lacking signed DPA",
            category="Third-Party",
            severity="medium",
            likelihood="medium",
            status="mitigating",
            owner="Procurement",
        )
        session.add(risk1)
        session.add(risk2)

        session.commit()
