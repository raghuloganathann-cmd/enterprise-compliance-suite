# Enterprise Compliance Suite (Base Scaffold)

A simple, extensible base project for tracking enterprise compliance activity:

- **Policies** — document/version register with owner and status
- **Compliance Requirements** — regulatory checklist mapped to frameworks (SOC 2, ISO 27001, GDPR, etc.)
- **Audits** — internal/external/regulatory audit scheduling and status
- **Risk Register** — identified risks with severity, likelihood, and mitigation status
- **Users** — basic role field (admin / auditor / risk_manager / viewer) as a stub for RBAC

## Stack

- **Backend:** FastAPI + SQLModel (SQLite by default, swappable for Postgres/MySQL)
- **Frontend:** Server-rendered Jinja2 dashboard (no build step required)
- **API docs:** auto-generated at `/docs` (Swagger UI) and `/redoc`

## Project structure

```
enterprise-compliance-suite/
├── app/
│   ├── main.py            # FastAPI app, dashboard route
│   ├── database.py        # engine, session, seed data
│   ├── models.py          # SQLModel entities
│   ├── routers/
│   │   ├── policies.py
│   │   ├── requirements.py
│   │   ├── audits.py
│   │   ├── risks.py
│   │   └── users.py
│   ├── templates/
│   │   ├── base.html
│   │   └── dashboard.html
│   └── static/
│       └── style.css
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:
- `http://localhost:8000/` — dashboard
- `http://localhost:8000/docs` — interactive API docs (create/update/delete records)

A SQLite file (`compliance_suite.db`) is created automatically on first run and seeded
with a few example policies, requirements, an audit, and two risk items so the dashboard
isn't empty on first load.

## Extending this base

This is intentionally minimal so it's easy to build on. Natural next steps:

- **Auth:** add real authentication (OAuth2/JWT) and enforce the `role` field on `User`
- **Evidence uploads:** attach files to `Audit` / `ComplianceRequirement` records (S3, local disk)
- **Notifications:** alert owners when a requirement lapses or a risk stays open past SLA
- **Framework templates:** pre-load requirement sets for specific frameworks (SOC 2, ISO 27001, HIPAA)
- **Audit trail:** log every change (who/when/what) for defensibility during external audits
- **Postgres:** swap `DATABASE_URL` in `app/database.py` for a production database
