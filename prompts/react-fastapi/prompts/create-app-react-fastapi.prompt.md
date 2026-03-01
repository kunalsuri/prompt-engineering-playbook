---
mode: 'agent'
description: 'Build My-SAAS-APP – A Full-Stack Feature-Driven SaaS application with React, TypeScript & FastAPI (JSON-based Auth)'
version: '1.0.0'
tags: [saas, full-stack, scaffolding, authentication]
stack: react-fastapi
patterns: [role-playing]
---

> **Learn why this works:** [Decomposition + Role-Playing](../../../learn/02-core-principles.md#22-principle-2-decomposition)

# Role

Act as a **Coding LLM** and **Principal Full-Stack Architect** building a **feature-based SaaS application** called **My-SAAS-APP**.

The app must be:

- Modern, modular, and **feature-driven**
- Full-stack: **React + TypeScript** frontend and **FastAPI** backend
- Using **JSON file storage** (no SQL DB) for users & sessions
- Ready as a **starter SaaS template** with **login, signup, landing page, and protected dashboard**

---

# Task

Build the My-SAAS-APP full-stack application according to the feature specifications below.

# Core Setup

## Tech Stack

- **Frontend**
  - React 18+ (TypeScript) with **Vite**
  - **Routing**: React Router v6
  - **Styling/UI**: Tailwind CSS + [shadcn/ui](https://ui.shadcn.com/) + Lucide Icons
  - **Fonts**: Inter / SF Pro Display
  - **State Management**
    - **React Query (TanStack Query)** → server state
    - **Zustand** → lightweight client state (auth/session, UI flags)

- **Backend**
  - Python 3.11+
  - **FastAPI** + **Pydantic v2**
  - **Uvicorn** as ASGI server
  - **NO traditional DB** (no Postgres/SQLite)
  - Custom **JSON Filesystem Storage** for:
    - `users.json`
    - `sessions.json`
    - Future feature-specific JSON files

- **Data & Media**
  - JSON persistence under `/backend/data`
  - (Optional, future) `/backend/media` for assets

- **Single Port Deployment**
  - The whole app (API + frontend) MUST run on **port 3031** in production.
  - **FastAPI serves the built React app** as static files.
  - All API routes are under `/api/*`.

---

# Monorepo Structure

Create this structure:

```text
My-SAAS-APP/
├── frontend/                        # React + TypeScript + Vite
│   └── src/
│       ├── features/                # Feature-based structure
│       │   └── user-profile/        # Example feature
│       │       ├── components/
│       │       ├── hooks/
│       │       └── index.ts
│       ├── components/              # Shared UI components
│       │   └── ui/                  # SHADCN COMPONENTS GO HERE (Button.tsx, etc)
│       ├── pages/                   # Page-level routes
│       │   ├── Landing.tsx
│       │   ├── Login.tsx
│       │   ├── Signup.tsx
│       │   └── Dashboard.tsx        # Modern dashboard with collapsable sidebar
│       ├── lib/
│       │   ├── api.ts               # API client (fetch/axios wrappers)
│       │   ├── utils.ts             # cn() helper for tailwind
│       │   └── state.ts             # Zustand + React Query setup
│       ├── types/                   # API/Domain types mirroring backend models
│       ├── App.tsx                  # Main app component (routes)
│       └── main.tsx                 # React entrypoint
│
├── backend/
│   ├── app/
│   │   ├── api/                     # FastAPI routers (all prefixed with /api)
│   │   │   ├── auth.py              # login/signup/logout, me
│   │   │   └── users.py             # basic user profile CRUD
│   │   ├── core/
│   │   │   ├── config.py            # settings, env loading
│   │   │   └── security.py          # password hashing, session id helpers
│   │   ├── db/
│   │   │   └── json_store.py        # ATOMIC JSON storage engine
│   │   ├── models/                  # Pydantic models
│   │   │   ├── user.py
│   │   │   ├── auth.py
│   │   │   └── session.py
│   │   ├── services/
│   │   │   ├── user_service.py      # user CRUD logic using JsonStore
│   │   │   └── session_service.py   # session create/validate/destroy
│   │   ├── main.py                  # FastAPI app, static mounting, CORS
│   │   └── __init__.py
│   ├── data/                        # JSON storage (git-ignored except templates)
│   │   ├── users.json               # created/seeded at startup
│   │   └── sessions.json
│   ├── requirements.txt
│   └── .env.example                 # environment config template
│
├── docs/
│   ├── PROJECT_STATUS.md            # REQUIRED implementation status
│   ├── QUICKSTART.md
│   ├── TECHNICAL.md
│   └── IMPLEMENTATION_SUMMARY.md
│
├── package.json                     # root scripts (optional: dev orchestration)
├── README.md                        # root-level documentation
└── .gitignore
````

---

- Use **feature-based folders** under `/frontend/src/features/*` for modular development.  
- Example: `/frontend/src/features/user-profile/` should handle all profile logic.  
- Ensure modularity so frontend and backend teams can work in parallel.

---

# **Style Guide**

### **Colors**

  - Primary: `#0070F3` (blue)  
  - Secondary: `#7928CA` (purple)  
  - Accent: `#FF0080`  
  - Dark: `#000000`  
  - Light: `#FFFFFF`  
  - Text (light): `#333333`  
  - Text (dark): `#FFFFFF`
 
### **UI/UX Patterns**
  - Fully Responsive design (desktop + mobile).  
  - Smooth transitions (dark/light mode).  
  - Reusable components that MUST use `shadcn/ui` such as cards, buttons, inputs.
  - Set up theme provider + Tailwind config before building pages

---

# Visual References
- GitHub landing pages (clean, developer-focused).  
- Vercel dashboard (professional, minimal). Modern, and latest with collapsable sidebar.
- Excalidraw (lightweight, intuitive interface).  

---

# Core Features

## 1\. Landing Page (`/`)

  * Clean, professional, GitHub-inspired layout
  * Sections:
      * Hero: app name, short tagline, CTA buttons (“Sign up”, “Login”)
      * Features section (3–4 cards)
      * Footer (simple)
  * Header:
      * Logo/title on left
      * Right: “Login”, “Sign up”, theme toggle
  * Theme toggle with React + Tailwind best practices

-----

## 2\. Authentication System

All persistence via **JSON files** in `/backend/data`. No SQL DB.

### Data Files

  * `users.json`:

    ```json
    {
      "schema_version": "1.0",
      "updated_at": "2025-11-29T10:30:00Z",
      "data": [
        {
          "id": "admin",
          "name": "Tim",
          "email": "admin@example.com",
          "username": "admin",
          "password_hash": "<hashed>",
          "role": "admin"
        }
      ]
    }
    ```

  * `sessions.json`:

    ```json
    {
      "schema_version": "1.0",
      "updated_at": "2025-11-29T10:30:00Z",
      "data": [
        {
          "session_id": "example-session-id-123",
          "user_id": "user1",
          "created_at": "2025-11-17T10:00:00Z",
          "demo": false
        }
      ]
    }
    ```

### Seeding Requirements

  * On backend startup:
      * Ensure `users.json` and `sessions.json` exist
      * Seed at least **4 users**
      * Include an **Admin Demo User** that always exists (by `id` or `email`)
      * Use **hashed passwords** (e.g., bcrypt) – plaintext only in comments, not in files

Example users (logical, not necessarily exact JSON):

  * admin / admin@example.com / role: admin
  * Alice / alice@example.com / role: HR
  * Leo / leo@example.com / role: IT
  * Eva / eva@example.com / role: manager

-----

## 3\. Authentication Flows

### Login Page (`/login`)

  * Fields: Email or username, Password
  * Buttons: **Login**, **Demo Login** (auto-login admin demo user)
  * Behavior:
      * On submit, call: `POST /api/auth/login`
      * On success:
          * Backend sets HTTP-only cookie with `session_id`
          * Frontend updates auth state (e.g., `isAuthenticated`, `user`)
          * Redirect to `/dashboard`
      * On error: Show clear error message (invalid credentials)

### Signup Page (`/signup`)

  * Fields: Name, Email, Username, Password, Confirm password
  * On submit:
      * Call `POST /api/auth/signup`
      * Validations: Email unique, Username unique, Password match
      * Backend: Adds user to `users.json`, generates ID, hashes password.

### Logout

  * Button in dashboard header
  * Calls `POST /api/auth/logout`
  * Backend: Removes session from `sessions.json`, clears cookie.
  * Frontend: Clears auth state, redirects to landing.

-----

## 4\. Sessions & Protected Routes

### Backend Session Handling

  * Use HTTP-only cookie: `session_id`
  * On each protected API call:
      * Read cookie, Validate in `sessions.json`.
      * If valid: attach `current_user` to request context.
      * If invalid/missing: return 401.

### Frontend Route Protection

  * `RequireAuth` component wrapper using React Router v6.
  * Checks auth state (Zustand + React Query).
  * On initial load: Call `GET /api/auth/me` to validate session.

-----

## 5\. Dashboard (`/dashboard`)

  * Layout: Collapsable **sidebar** (shadcn/ui), Top navbar (Title, Theme Toggle, User Avatar).
  * Content:
      * “Welcome, {user.name}” card
      * “Your account”, “Recent activity”, “Coming soon”

-----

## 6\. User Profile Feature (`/frontend/src/features/user-profile/`)

  * View and edit: Name, Email, Username.
  * Show role (read-only).
  * API: `GET /api/users/me`, `PUT /api/users/me`
  * Persistence: Use `JsonStore` on backend to update `users.json`.

-----

# JSON Storage Engine (CRITICAL)

Implement a **robust JSON storage layer**: `backend/app/db/json_store.py`.

## JsonStore Requirements

  * **Atomic Writes**: Write to `*.tmp` -\> Validate JSON -\> Backup old -\> `os.rename()` to replace.
  * **Concurrency Protection**: Use `filelock` library. Lock file per JSON file.
  * **Corruption Recovery**: On load failure, try backup, else init empty structure.
  * **File Schema**: Standard wrapper with `schema_version` and `data` list.
  * Helper methods: `load()`, `save(data)`, `get_all()`, `find(predicate)`.

-----

# Backend API Design (FastAPI)

Base path: all routes under `/api/*`.

## Auth Endpoints (`/api/auth`)

  * `POST /signup`, `POST /login`, `POST /logout`
  * `GET /me`: Returns current authenticated user based on cookie.

## User Endpoints (`/api/users`)

  * `GET /me`, `PUT /me` (Update profile)

-----

# Deployment & Config (Port 3031)

## Backend `main.py` Requirements

  * Create `FastAPI` instance.
  * Include routers (`auth`, `users`) with prefix `/api`.
  * **CORS**: Enable for `http://localhost:5173` (Vite dev) and `http://localhost:3031`.
  * **Static Files (Production)**:
      * Mount `frontend/dist` as static files at root `/`.
      * **SPA Fallback**: Add a route that catches any 404 (non-API) and serves `frontend/dist/index.html`.

## Vite Config (Frontend)

  * Build output directory: `frontend/dist`.
  * **Dev Proxy (CRITICAL)**:
      * Configure `vite.config.ts` server proxy so requests to `/api` are forwarded to `http://localhost:8000` (or whichever port backend runs on in dev) to avoid CORS issues during development.

-----

# Environment & Config

Create `backend/.env.example`:

```bash
APP_NAME=My-SAAS-APP
APP_ENV=development
APP_PORT=3031
SECRET_KEY=change-this-secret
DATA_DIR=./backend/data
FRONTEND_DIST=../../frontend/dist
SESSION_COOKIE_NAME=session_id
```

-----

# Documentation

Create `docs/PROJECT_STATUS.md` immediately after generation tracking completed items.

-----

# Output Format

Generate a **complete starter SaaS monorepo** with:

  * React + TypeScript + Vite frontend (feature-based)
  * FastAPI backend with JSON storage and robust `JsonStore`
  * Auth system (login, signup, logout, sessions) using HTTP-only cookies
  * Single-port deployment on **3031** with FastAPI serving both API and frontend.

**IMPORTANT:** Start by generating the **file structure** and the **critical configuration files** (vite config, requirements.txt, backend main.py, json\_store.py), then move to features.

---
