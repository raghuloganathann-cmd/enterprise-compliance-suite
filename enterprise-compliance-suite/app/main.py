"""
Enterprise Compliance Suite - Main Application
------------------------------------------------
A simple base FastAPI project for managing enterprise compliance:
- Policies (document/version tracking)
- Compliance Requirements (regulatory checklist items)
- Audits (scheduled & completed audit records)
- Risk Register (identified risks with severity/status)
- Users & Roles (basic RBAC)

Run with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.database import init_db, get_session
from app.models import Policy, ComplianceRequirement, Audit, RiskItem, User
from app.routers import policies, requirements, audits, risks, users

app = FastAPI(
    title="Enterprise Compliance Suite",
    description="Base scaffold for tracking policies, compliance requirements, audits, and risk.",
    version="0.1.0",
)

# Static & templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# API routers
app.include_router(policies.router)
app.include_router(requirements.router)
app.include_router(audits.router)
app.include_router(risks.router)
app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, session: Session = Depends(get_session)):
    """Simple dashboard summarizing compliance posture."""
    policies = session.exec(select(Policy)).all()
    requirements = session.exec(select(ComplianceRequirement)).all()
    audits = session.exec(select(Audit)).all()
    risks = session.exec(select(RiskItem)).all()

    stats = {
        "total_policies": len(policies),
        "total_requirements": len(requirements),
        "met_requirements": len([r for r in requirements if r.status == "met"]),
        "open_audits": len([a for a in audits if a.status != "completed"]),
        "high_risks": len([r for r in risks if r.severity in ("high", "critical") and r.status != "closed"]),
        "total_risks": len(risks),
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "stats": stats,
            "policies": policies[:5],
            "risks": sorted(risks, key=lambda r: r.severity_rank, reverse=True)[:5],
            "audits": audits[:5],
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}
