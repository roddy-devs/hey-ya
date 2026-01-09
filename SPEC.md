# Ice Cold Beer Scorekeeper — Functional Specification

## Overview
Ice Cold Beer Scorekeeper is a mobile-first web application for tracking performance in the arcade game *Ice Cold Beer*. The app records detailed play-session data including time tracking, per-hole scoring with time-based decay, ball drops, completed loops, and long-term statistics. The primary use case is live tracking during play on a mobile device, with secondary desktop usage for reviewing stats.

---

## Tech Stack
- Backend: Django + Django REST Framework
- Frontend: React
- Database: PostgreSQL
- Containerization: Docker + Docker Compose
- Backend Dependency Management: Poetry (no venv)
- Frontend Package Manager: npm (Node.js)
- Hosting: Single AWS EC2 instance
- Protocol: HTTPS
- Configuration: Environment variables via `.env`

---

## Core Concepts

### Users
- Use Django’s built-in authentication system
- Users are stored in PostgreSQL
- Each play session belongs to exactly one user
- Users can view only their own sessions and stats

---

### Session
A Session represents one continuous play session, which may include multiple loops.

Session fields:
- `user`
- `start_time`
- `end_time` (nullable while active)
- `duration` (derived)
- `total_score`
- `total_ball_drops`
- `total_loops`
- `created_at`

Rules:
- Session starts manually
- Session ends manually
- Completed sessions are immutable

---

### Loops
A loop is completed each time the ball is successfully placed into **hole 10**.

Loop rules:
- Completing hole 10 increments `total_loops`
- After hole 10, hole progression resets to hole 1
- Score, timing, and drops continue accumulating across loops
- Loops are a primary performance metric

---

### Holes
Each session consists of repeated sequences of 10 holes.

Each hole attempt tracks:
- `session`
- `loop_index`
- `hole_number` (1–10)
- `start_time`
- `end_time`
- `completion_time` (derived)
- `base_score`
- `decay_score`
- `final_score`
- `ball_drops`

Rules:
- Only one hole is active at a time
- Hole timing starts when the hole becomes active
- Hole timing ends when the ball enters the hole
- Hole 10 completion triggers a loop increment

---

## Time Tracking

### Session Timing
- Session timer starts at session start
- Runs continuously until session end
- Duration derived from timestamps

### Hole Timing
- Each hole records start and end times
- Completion time is stored per hole
- Time data is first-class and must be accurate
- Used for score decay and analytics

---

## Scoring Logic
- Each hole has a predefined base score
- Score decays based on hole completion time
- Decay logic must be deterministic and configurable
- Final score per hole cannot go below zero
- Total score is cumulative across all holes and loops

---

## Ball Drops
- Ball drops are manually recorded
- Drops are tracked per hole
- Aggregated at the session level
- Drops do not affect score directly (for now)

---

## Frontend UX Requirements

### Primary View — Live Scoreboard
Used during active gameplay.

Display:
- Current loop count
- Current hole number
- Session timer
- Current hole timer
- Current hole score
- Total score
- Ball drops (current hole and total)

Controls:
- Start session
- Advance hole (record completion)
- Record ball drop
- End session

Design goals:
- Large, touch-friendly controls
- High contrast
- Arcade / LED-style scoreboard aesthetic
- Minimal distraction during play

---

### Secondary Views

#### Session History
- List completed sessions
- Show date, duration, total score, total loops, total drops

#### Session Detail
- Per-loop breakdown
- Per-hole times, scores, and drops

#### Stats View
Aggregate user statistics:
- Best score
- Worst score
- Average score
- Average loops per session
- Fastest completion time per hole
- Average completion time per hole

---

## Data Persistence
- PostgreSQL is the source of truth
- All session, hole, loop, and user data is persisted
- No loss of data on refresh or restart

---

## API Design
RESTful endpoints must support:
- User authentication
- Creating and ending sessions
- Recording hole completion
- Incrementing loops
- Recording ball drops
- Fetching session history
- Fetching detailed session data
- Fetching aggregate stats

---

## Containerization & Runtime

### Docker Requirements
- Use Docker and Docker Compose
- Services:
  - Backend (Django + DRF)
  - Frontend (React)
  - Database (PostgreSQL)
- PostgreSQL data persisted via Docker volumes
- Docker Compose is the canonical runtime definition

---

## Dependency Management

### Backend
- Use Poetry exclusively
- No `venv` or `virtualenv`
- Include:
  - `pyproject.toml`
  - `poetry.lock`
- Django commands must be runnable via Poetry

### Frontend
- React app using Node.js + npm
- Frontend can run locally or inside Docker
- Docker is required for production parity

---

## One-Command Startup
The repository must include a single command to start the full stack.

The command must:
- Build Docker images if needed
- Start backend, frontend, and database
- Apply database migrations
- Be usable locally and on EC2

Examples:
- `docker compose up --build`
- `./start.sh`
- `make up`

Goal:
**Clone repo → one command → app running**

---

## Deployment (AWS EC2)

- Single EC2 instance
- Linux host
- Docker and Docker Compose installed
- App deployed by cloning the repo and running Docker Compose
- Environment variables provided via `.env`
- PostgreSQL runs in Docker
- HTTPS must be configured (e.g. reverse proxy + TLS)

Documentation must include:
- EC2 setup
- Docker installation
- `.env` configuration
- Port and security group setup
- HTTPS configuration
- Restart behavior after reboot

---

## Documentation Requirements
The repository must include:
- `README.md`
- Clear instructions for:
  - Local development
  - Docker usage
  - Poetry usage
  - npm usage
  - One-command startup
  - EC2 deployment
  - HTTPS setup

Documentation should favor explicit commands over prose.

---

## Non-Goals
- No automated machine integration
- No anti-cheat enforcement
- No real-time multiplayer
- No scaling beyond a single EC2 instance

---

## Guiding Principles
- Track what matters to real play
- Time and loops are core skill indicators
- Accuracy over speed
- Simplicity over abstraction
- Never distract the player mid-session
