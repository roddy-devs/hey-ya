# Copilot Instructions

This repository contains a full-stack web application called **Ice Cold Beer Scorekeeper**.

Copilot should follow the functional and architectural requirements defined in `SPEC.md`.

Key constraints:
- Backend: Django + Django REST Framework
- Frontend: React (npm / Node.js)
- Database: PostgreSQL
- Dependency management: Poetry (no venv)
- Runtime: Docker + Docker Compose
- Hosting target: Single AWS EC2 instance with HTTPS
- Mobile-first UI

Core domain concepts:
- Users
- Sessions
- Holes (1–10)
- Loops (completed on hole 10)
- Time tracking (session + per-hole)
- Time-based score decay

Favor clarity, correctness, and explicit logic over clever abstractions.
Do not introduce additional infrastructure or tooling unless specified in the spec.
Adhere to best practices for security, performance, and maintainability in web applications.