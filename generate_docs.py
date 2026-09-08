import os
import json
import shutil

base_dir = "/Volumes/Fullstack/Github/XAI-Guard/docs"

phases_data = [
    {
        "folder": "01-product",
        "title": "PHASE 01 — Product Foundation",
        "sub_phases": [
            "01.01 Existing Product Audit",
            "01.02 Product Problem Definition",
            "01.03 Target User Definition",
            "01.04 Core Service Definition",
            "01.05 Feature Mapping",
            "01.06 Product Boundaries",
            "01.07 XAI Value Proposition",
            "01.08 Model Comparison Strategy",
            "01.09 Success Criteria",
            "01.10 Phase Validation"
        ]
    },
    {
        "folder": "02-user-journey",
        "title": "PHASE 02 — User Journey",
        "sub_phases": [
            "02.01 User Persona: Security Analyst",
            "02.02 User Persona: ML Engineer",
            "02.03 User Persona: Admin",
            "02.04 Data Ingestion Flow",
            "02.05 Threat Detection Flow",
            "02.06 Threat Investigation Flow",
            "02.07 Model Comparison Flow",
            "02.08 Reporting Flow",
            "02.09 System Configuration Flow",
            "02.10 Phase Validation"
        ]
    },
    {
        "folder": "03-architecture",
        "title": "PHASE 03 — System Architecture",
        "sub_phases": [
            "03.01 Existing Architecture Audit",
            "03.02 Application Boundaries",
            "03.03 Backend Architecture",
            "03.04 Frontend Architecture",
            "03.05 ML Boundary",
            "03.06 Database Boundary",
            "03.07 API Flow",
            "03.08 Security Boundary",
            "03.09 Observability Strategy",
            "03.10 Architecture Validation"
        ]
    },
    {
        "folder": "04-database",
        "title": "PHASE 04 — Database Foundation",
        "sub_phases": [
            "04.01 Database Architecture & Technology Selection",
            "04.02 Users & Roles Schema",
            "04.03 Datasets & Data Versions Schema",
            "04.04 Models & Experiments Schema",
            "04.05 Predictions & Explanations Schema",
            "04.06 Reports & Analytics Schema",
            "04.07 Audit Logs Schema",
            "04.08 Alembic Migrations Setup",
            "04.09 Database Seeding Strategy",
            "04.10 Database Validation"
        ]
    },
    {
        "folder": "05-api",
        "title": "PHASE 05 — Core API Endpoints",
        "sub_phases": [
            "05.01 API Design & OpenAPI Spec",
            "05.02 Authentication Endpoints (/auth)",
            "05.03 User Management Endpoints (/users)",
            "05.04 Dataset Endpoints (/datasets)",
            "05.05 Model Registry Endpoints (/models)",
            "05.06 Inference Endpoints (/predictions)",
            "05.07 XAI Endpoints (/explanations)",
            "05.08 Analytics Endpoints (/analytics)",
            "05.09 Admin & Audit Endpoints (/admin)",
            "05.10 API Validation"
        ]
    },
    {
        "folder": "06-frontend",
        "title": "PHASE 06 — Frontend Foundation",
        "sub_phases": [
            "06.01 Next.js Workspace Setup",
            "06.02 Shared UI Package Configuration",
            "06.03 State Management Strategy (Zustand)",
            "06.04 Data Fetching & Caching (TanStack Query)",
            "06.05 API Client Generator",
            "06.06 Form Handling & Validation",
            "06.07 Authentication Flow Integration",
            "06.08 Routing & Layout Architecture",
            "06.09 Error Handling & Error Boundaries",
            "06.10 Frontend Validation"
        ]
    },
    {
        "folder": "07-ui-ux",
        "title": "PHASE 07 — UI/UX Implementation",
        "sub_phases": [
            "07.01 Design System & Typography",
            "07.02 Shadcn & Tailwind Configuration",
            "07.03 Base Components Implementation",
            "07.04 Main Website Layout",
            "07.05 Dashboard Layout",
            "07.06 Data Table Components",
            "07.07 Chart & Visualization Components",
            "07.08 XAI Component Library",
            "07.09 Responsive & Accessibility Pass",
            "07.10 UI/UX Validation"
        ]
    },
    {
        "folder": "08-ml-integration",
        "title": "PHASE 08 — ML Integration",
        "sub_phases": [
            "08.01 ML Artifact Structure Audit",
            "08.02 Model Loading Service",
            "08.03 Preprocessing Pipeline Integration",
            "08.04 Feature Engineering API Wrapper",
            "08.05 Synchronous Inference Engine",
            "08.06 Asynchronous Batch Inference (Celery)",
            "08.07 Model Versioning & Registry Connect",
            "08.08 Latency & Throughput Tracking",
            "08.09 Error Handling in ML Pipeline",
            "08.10 ML Integration Validation"
        ]
    },
    {
        "folder": "09-model-comparison",
        "title": "PHASE 09 — Model Comparison",
        "sub_phases": [
            "09.01 Comparison Metrics Definition",
            "09.02 Live Inference Runner",
            "09.03 Evaluation API Integration",
            "09.04 Model Comparison UI Grid",
            "09.05 Performance vs Latency Visualization",
            "09.06 Cost & Efficiency Estimator",
            "09.07 Champion/Challenger Dashboard",
            "09.08 A/B Testing Infrastructure",
            "09.09 Model Selection Flow",
            "09.10 Model Comparison Validation"
        ]
    },
    {
        "folder": "10-xai",
        "title": "PHASE 10 — Explainable AI (XAI)",
        "sub_phases": [
            "10.01 XAI Product Strategy",
            "10.02 SHAP Integration & API",
            "10.03 LIME Integration & API",
            "10.04 Transformer Attention API",
            "10.05 Human-readable Explanation Generator",
            "10.06 Feature Importance UI Component",
            "10.07 Attention Map UI Component",
            "10.08 Prediction Details Page",
            "10.09 XAI Latency Optimization",
            "10.10 XAI Validation"
        ]
    },
    {
        "folder": "11-analytics",
        "title": "PHASE 11 — Analytics & Threat Detection",
        "sub_phases": [
            "11.01 Threat Detection Heuristics",
            "11.02 Risk Scoring Calculator",
            "11.03 Real-time Events Dashboard",
            "11.04 Time-series Threat Analytics",
            "11.05 Geographic & IP Analytics",
            "11.06 Threat Investigation Workflow",
            "11.07 False Positive/Negative Feedback Loop",
            "11.08 Alert Triage System",
            "11.09 Historical Analysis Tools",
            "11.10 Analytics Validation"
        ]
    },
    {
        "folder": "12-reports",
        "title": "PHASE 12 — Reporting System",
        "sub_phases": [
            "12.01 Report Types Definition",
            "12.02 PDF Generation Engine",
            "12.03 CSV/Excel Export Engine",
            "12.04 Scheduled Reports (Cron)",
            "12.05 Compliance Reporting (SOC2/GDPR)",
            "12.06 Model Performance Reports",
            "12.07 Threat Intelligence Reports",
            "12.08 Report Delivery Service (Email)",
            "12.09 Report Archive & History",
            "12.10 Reporting Validation"
        ]
    },
    {
        "folder": "13-admin",
        "title": "PHASE 13 — Admin Portal",
        "sub_phases": [
            "13.01 Admin Dashboard Layout",
            "13.02 User & Role Management",
            "13.03 System Health Monitoring",
            "13.04 ML Model Management Panel",
            "13.05 Model Deployment Approval Flow",
            "13.06 Audit Log Viewer",
            "13.07 System Configuration Settings",
            "13.08 Feature Flag Management",
            "13.09 Resource Usage Analytics",
            "13.10 Admin Validation"
        ]
    },
    {
        "folder": "14-security",
        "title": "PHASE 14 — Security Engineering",
        "sub_phases": [
            "14.01 RBAC Implementation",
            "14.02 JWT & Session Hardening",
            "14.03 API Rate Limiting",
            "14.04 Input Validation & Sanitization",
            "14.05 File Upload Security (Datasets)",
            "14.06 Secret Management (Vault/.env)",
            "14.07 Database Row-level Security",
            "14.08 Model Artifact Tamper Protection",
            "14.09 Dependency Scanning & SAST",
            "14.10 Security Validation"
        ]
    },
    {
        "folder": "15-testing",
        "title": "PHASE 15 — Testing Strategy",
        "sub_phases": [
            "15.01 Unit Testing Setup (Pytest & Jest)",
            "15.02 Backend Integration Tests",
            "15.03 API Contract Tests",
            "15.04 Frontend Component Tests",
            "15.05 State Management Tests",
            "15.06 ML Inference Tests",
            "15.07 E2E Testing Setup (Playwright/Cypress)",
            "15.08 Security & Auth Tests",
            "15.09 CI/CD Test Automation",
            "15.10 Testing Coverage Validation"
        ]
    },
    {
        "folder": "16-performance",
        "title": "PHASE 16 — Performance Engineering",
        "sub_phases": [
            "16.01 Performance Baselines & Targets",
            "16.02 API Latency Optimization",
            "16.03 Database Query Optimization",
            "16.04 ML Inference Optimization (ONNX)",
            "16.05 Caching Strategy (Redis)",
            "16.06 Frontend Bundle Optimization",
            "16.07 Edge Caching / CDN",
            "16.08 Async Task Workers Optimization",
            "16.09 Large Dataset Processing",
            "16.10 Performance Validation"
        ]
    },
    {
        "folder": "17-devops",
        "title": "PHASE 17 — DevOps & Infrastructure",
        "sub_phases": [
            "17.01 Docker Containerization",
            "17.02 Docker Compose Local Environment",
            "17.03 CI/CD Pipeline (GitHub Actions)",
            "17.04 Infrastructure as Code (Terraform)",
            "17.05 Kubernetes Manifests Setup",
            "17.06 Database Migration Pipeline",
            "17.07 Secrets Injection",
            "17.08 Model Registry Cloud Sync",
            "17.09 Multi-environment Strategy (Dev/Staging/Prod)",
            "17.10 Infrastructure Validation"
        ]
    },
    {
        "folder": "18-production",
        "title": "PHASE 18 — Production Readiness",
        "sub_phases": [
            "18.01 Production Environment Provisioning",
            "18.02 Monitoring Setup (Prometheus/Grafana)",
            "18.03 Centralized Logging (ELK/Loki)",
            "18.04 Alerting & PagerDuty Integration",
            "18.05 Disaster Recovery & Backups",
            "18.06 Model Drift Detection in Prod",
            "18.07 Incident Response Playbook",
            "18.08 Production Load Testing",
            "18.09 Staging to Production Promotion",
            "18.10 Final Production Sign-off"
        ]
    }
]

def generate_sub_phase_content(phase_idx, sub_phase_idx, sub_phase_title, phase_title):
    next_phase_str = f"Phase {phase_idx+1:02d}.{(sub_phase_idx+2):02d}" if (sub_phase_idx+1) < 10 else (f"Phase {(phase_idx+2):02d}.01" if (phase_idx+1) < len(phases_data) else "Completion")
    
    return f"""### {sub_phase_title}

#### Objective
To successfully implement {sub_phase_title.split(' ', 1)[1]} as part of {phase_title}. This ensures that the platform correctly handles this component in the end-to-end lifecycle.

#### Why
This is required because without it, the product layer remains incomplete and disconnected from the underlying ML engine. It fulfills a critical requirement for a production-grade Explainable AI Cybersecurity Platform.

#### Prerequisites
- All previous phases up to {(phase_idx+1):02d}.{sub_phase_idx:02d} must be completed.
- Existing ML repository structure must be intact.

#### Depends On
{(phase_idx+1):02d}.{sub_phase_idx:02d} (or previous phase if this is the first sub-phase).

#### Files / Modules
- `apps/` frontend boundaries (web/admin)
- `services/api/` (FastAPI backend)
- Database schema / Redis store
- ML artifacts (`ml/artifacts/`)

#### What To Implement
1. Analyze existing research/ML code related to this sub-phase.
2. Design the product layer (API, Schema, UI).
3. Connect the frontend to the backend API.
4. Integrate the ML component where applicable.

#### How To Implement
1. **Design**: Draft the interface or schema.
2. **Backend**: Implement the FastAPI route and SQLAlchemy model.
3. **ML Integration**: Load the required artifacts or utilities from the `ml/` package.
4. **Frontend**: Create the UI components in Next.js using shadcn/ui.
5. **State**: Connect via TanStack Query / Zustand.

#### Data Flow
USER -> Next.js Frontend -> FastAPI -> Database/Redis -> ML Inference/XAI Engine -> Response -> USER

#### API / Backend Impact
Requires endpoints to handle requests securely, validate input with Pydantic, and process the logic asynchronously if latency > 500ms.

#### Frontend / UI Impact
Requires responsive, accessible components displaying loading/error/success states.

#### Database Impact
May require Alembic migrations and new SQLAlchemy models to persist state.

#### ML Impact
Leverages the existing working ML implementation. The models, preprocessing, and XAI utilities are treated as read-only or invoked via wrappers.

#### Security Considerations
- Input validation (Pydantic).
- RBAC authorization checks.
- Sanitization of data.
- Rate limiting.

#### Testing
- Unit tests for logic.
- Integration tests for API.
- E2E tests for UI flows.

#### Validation
Developer must manually verify the UI flow, check the database records, and verify API responses in Swagger/Postman.

#### Expected Result
A fully functioning {sub_phase_title.split(' ', 1)[1]} feature that integrates smoothly into the larger cybersecurity platform.

#### Completion Criteria
- [ ] Code implemented.
- [ ] Tests passing.
- [ ] Security reviewed.
- [ ] API documented.
- [ ] UI states handled (loading, error, empty).

#### Next Step
Proceed to {next_phase_str} to continue the implementation sequence.
"""

def main():
    if os.path.exists(base_dir):
        # Move existing to _archive
        archive_dir = os.path.join(base_dir, "_archive_new")
        os.makedirs(archive_dir, exist_ok=True)
        for item in os.listdir(base_dir):
            if item != "_archive_new" and item != "_archive":
                shutil.move(os.path.join(base_dir, item), archive_dir)
    else:
        os.makedirs(base_dir, exist_ok=True)

    # 00-project-audit
    audit_dir = os.path.join(base_dir, "00-project-audit")
    os.makedirs(audit_dir, exist_ok=True)
    with open(os.path.join(audit_dir, "00-audit-report.md"), "w") as f:
        f.write("# Project Audit Report\n\n## Overview\nThis audit confirms the ML implementation exists and is functional. The product layer is missing and this documentation provides the blueprint to build it.\n")

    # Generate phases 1-18
    for i, phase in enumerate(phases_data):
        phase_dir = os.path.join(base_dir, phase["folder"])
        os.makedirs(phase_dir, exist_ok=True)
        
        file_path = os.path.join(phase_dir, f"{phase['folder']}.md")
        with open(file_path, "w") as f:
            f.write(f"# {phase['title']}\n\n")
            
            for j, sub in enumerate(phase["sub_phases"]):
                content = generate_sub_phase_content(i, j, sub, phase["title"])
                f.write(content + "\n---\n\n")

    # 19-roadmap
    roadmap_dir = os.path.join(base_dir, "19-roadmap")
    os.makedirs(roadmap_dir, exist_ok=True)
    with open(os.path.join(roadmap_dir, "MASTER-ROADMAP.md"), "w") as f:
        f.write("# MASTER ROADMAP\n\n")
        f.write("| Phase | Sub-phase | Status |\n|---|---|---|\n")
        for phase in phases_data:
            for sub in phase["sub_phases"]:
                f.write(f"| {phase['title']} | {sub} | [ ] |\n")

    # 20-ai-development-prompts
    prompts_dir = os.path.join(base_dir, "20-ai-development-prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    for i, phase in enumerate(phases_data):
        with open(os.path.join(prompts_dir, f"{phase['folder']}-prompt.md"), "w") as f:
            f.write(f"""# AI Coding Agent Prompt: {phase['title']}

## ROLE
Act as a Senior Full-Stack Engineer and ML Platform Architect.

## PROJECT CONTEXT
Explainable Transformer-Based Intelligent Threat Detection & Risk Analytics Platform.

## CURRENT STATE
ML layer works. Product layer is missing.

## PHASE
{phase['title']}

## OBJECTIVE
Implement the sub-phases defined in `{phase['folder']}.md`.

## DEPENDENCIES
Phase {(i):02d} must be complete.

## FILES TO INSPECT
- `apps/`
- `services/api/`
- `ml/`

## FILES TO MODIFY
(Determine based on sub-phase)

## IMPLEMENTATION STEPS
Follow the 18-step guide in the documentation strictly.

## CONSTRAINTS
Do not rebuild existing ML code.

## SECURITY REQUIREMENTS
Implement RBAC, validate inputs, check permissions.

## TESTING REQUIREMENTS
Unit, Integration, E2E.

## VALIDATION
Verify all UI states and API responses.

## EXPECTED OUTPUT
A complete, functioning feature.

## DEFINITION OF DONE
Implementation + Tests + Validation + Security Checked + Acceptance Criteria Satisfied.

## NEXT STEP
Report changes and proceed to next sub-phase.
""")

    # MASTER-PROJECT-SPECIFICATION.md
    with open(os.path.join(base_dir, "MASTER-PROJECT-SPECIFICATION.md"), "w") as f:
        f.write("""# MASTER PROJECT SPECIFICATION

## Overview
Explainable Transformer-Based Intelligent Threat Detection & Risk Analytics Platform.

## Core Goal
Transition the project from a working ML research repository into a complete, production-grade cybersecurity platform.

## Key Principles
1. **Preserve ML**: The existing ML code is working and should not be rewritten.
2. **Product Focus**: Build the missing service layer (API, DB, UI).
3. **Execution Ready**: Follow the 18 phases defined in this documentation strictly in order.
4. **XAI & Comparison**: Expose explainability and model comparison directly to the end-users.

## Folder Structure
See `docs/` directories `00` through `20` for phase-by-phase implementation blueprints.
""")

if __name__ == "__main__":
    main()
