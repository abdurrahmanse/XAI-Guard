# Definition of Done (DoD)

To prevent partially finished work from halting the critical path, every phase must meet its specific category's Definition of Done before progressing.

## 1. ML Experiment Phase (DoD)
- [ ] Model architecture script is checked into `ml/src/models/`.
- [ ] Hyperparameter search completed via Optuna and logged to MLflow.
- [ ] Final trained artifact is registered in the MLflow Model Registry.
- [ ] Pillar 1, 2, and 3 metrics are populated in the Registry tags.
- [ ] Analysis Jupyter Notebook is committed to `ml/notebooks/`.
- [ ] The research findings document is updated with the per-attack-type F1 table.

## 2. API Backend Module Phase (DoD)
- [ ] All specified endpoints are implemented in the `router.py`.
- [ ] Input/Output validation is strictly enforced via Pydantic (`schemas.py`).
- [ ] Business logic is isolated in `service.py` (no database calls in routers).
- [ ] Database interactions utilize `asyncpg` and SQLAlchemy 2.0.
- [ ] OpenAPI (Swagger) specification generates without errors.
- [ ] `pytest` module coverage is $\ge 80\%$.

## 3. Frontend Application Phase (DoD)
- [ ] UI built utilizing Next.js 15, React 19, Tailwind CSS 4, and shadcn/ui.
- [ ] Global state is strictly managed via Zustand.
- [ ] Async server state and caching is managed via TanStack Query v5.
- [ ] Zod schemas perfectly mirror the Backend Pydantic schemas.
- [ ] Accessibility (a11y) passes Chrome DevTools audits.
- [ ] End-to-End Playwright test covering the user workflow executes successfully.

## 4. Infrastructure & Architecture Phase (DoD)
- [ ] Resource is formally defined (e.g., Docker Compose, ADR, Schema).
- [ ] Containers boot successfully and pass health checks on a clean machine.
- [ ] Documentation is updated, linking to the relevant Glossary or ADR files.
- [ ] No manual UI configuration is required (100% Infrastructure as Code).
