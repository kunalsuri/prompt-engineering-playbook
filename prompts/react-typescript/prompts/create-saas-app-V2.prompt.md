---
mode: 'agent'
description: 'Build My-SAAS-APP – A Full-Stack Feature-Driven SaaS application with React, TypeScript & Express'
version: '1.1.0'
changelog:
  - version: '1.1.0'
    date: '2025-06-01'
    changes: 'Refined execution rules, improved output structure, and added quality-gate checks'
  - version: '1.0.0'
    date: '2025-01-15'
    changes: 'Initial release'
---

> **Learn why this works:** [Decomposition + Specificity](../../../learn/02-core-principles.md#22-principle-2-decomposition)

# Role

Act as a **Coding LLM** with the role of an **expert full-stack engineer** building a **feature-based SaaS application**.
The application must be modern, modular, scalable, and ready for real SaaS projects.

---

# Task

Build the My-SAAS-APP application according to the feature specifications below, implementing all sections to produce a complete, working monorepo.

# **Core Setup**

* **Stack**: React (TypeScript) + Express (TypeScript)
* **Bundler**: **Vite**
* **Routing**: **React Router**
* **Styling/UI**: TailwindCSS + [shadcn/ui](https://ui.shadcn.com/) + Lucide Icons
* **Fonts**: Inter / SF Pro Display
* **Design Language**: Card-based UI, responsive grid, smooth theme transitions
* **State Management**:

  * **React Query** → server state
  * **Zustand** → lightweight client state

* **Server Configuration**:
  * **CRITICAL**: Both frontend and backend MUST run on the **same port** 3031 for ease of development
  * Express serves the built React app as static files

---

# **Monorepo Structure**

My-SAAS-APP/
├── client/                          # React + TypeScript frontend
│   └── src/
│       ├── features/                # Feature-based structure
│       │   └── user-profile/        # User profile module
│       │       ├── components/      # Feature-specific components
│       │       ├── hooks/           # Feature-specific hooks
│       │       └── index.ts         # Entry for feature
│       ├── components/              # Shared UI components / wrappers (no naming collisions with shadcn/ui)
│       ├── pages/                   # Page-level routes
│       │   ├── Landing.tsx
│       │   ├── Login.tsx
│       │   ├── Signup.tsx
│       │   └── Dashboard.tsx        # Modern, latest with collapsable sidebar
│       ├── lib/                     # Client utilities
│       │   ├── api.ts               # API calls (fetch wrappers)
│       │   └── state.ts             # Zustand/React Query setup
│       ├── App.tsx                  # Main app component
│       └── main.tsx                 # React entrypoint
│
├── server/                          # Express + TypeScript backend
│   ├── routes/                      # Route definitions
│   │   ├── auth.ts
│   │   ├── users.ts
│   │   └── sessions.ts
│   ├── controllers/                 # Route handlers/business logic
│   │   ├── authController.ts
│   │   └── userController.ts
│   ├── middleware/                  # Middleware functions
│   │   └── authMiddleware.ts
│   ├── utils/                       # Helpers
│   │   ├── fileStorage.ts           # Read/write JSON helpers
│   │   └── validation.ts
│   ├── seed/
│   │   └── seedUsers.ts             # Startup seeding logic
│   └── server.ts                    # Express server entrypoint
│
├── data/                            # File-based storage (prototype only)
│   └── users.json                   # User + session storage
│   └── sessions.json
│
├── docs/                            # Documentation folder (REQUIRED)
│   ├── PROJECT_STATUS.md            # Implementation status with timestamp (REQUIRED)
│   ├── QUICKSTART.md                # Quick setup guide
│   ├── TECHNICAL.md                 # Technical documentation
│   └── IMPLEMENTATION_SUMMARY.md    # Architecture details
│
├── package.json
├── tsconfig.json
└── README.md                        # Main readme (root level only)


- Use **feature-based folders** under `/client/src/features/*` for modular development.  
- Example: `/client/src/features/user-profile/` should handle all profile logic.  
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
 
### **UI/UX Patterns**
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

# **Features**

## **Landing Page**

- Clean, professional, GitHub-inspired layout
- Light/dark theme toggle using React best practices.

---

## **Dashboard**

- Must replicate the **layout & style from GitHub**.  
- Sidebar, dashboard, and other UI elements must use **shadcn/ui** components.  
- Modular and future-ready (feature-based).  
- Dark/light theme supported out of the box.   

---

# **User Profile Feature**

  Located at: `/client/src/features/user-profile/`
  * Edit + save profile data
  * Sync updates to `users.json` → `"users"` array
  * Maintain full front-back separation

---

# **User Data Seeding (`/data/users.json`)**

### Requirements

* Ensure `users.json` exists at server startup
* Ensure **minimum 4 seeded users** exist
* The **Admin Demo User must always remain**
* Implement seeding in `server/seed/seedUsers.ts`
* Run seeding before the server starts listening

### Seeded Users (example)

```json
{
  "users": [
    { "id": "admin", "name": "Tim", "email": "admin@example.com", "password_hash": "$2b$12$LJ3m4ys3Lk...", "role": "admin" },
    { "id": "user1", "name": "Alice", "email": "alice@example.com", "password_hash": "$2b$12$Xy9k2bR7Qp...", "role": "HR" },
    { "id": "user2", "name": "Leo", "email": "leo@example.com", "password_hash": "$2b$12$Nm4z8wVt1s...", "role": "IT" },
    { "id": "manager1", "name": "Eva", "email": "eva@example.com", "password_hash": "$2b$12$Qr5j6kL9Hw...", "role": "manager" }
  ]
}
```
*(Passwords are bcrypt-hashed. Use a library like `bcryptjs` to hash on signup and compare on login.)*

---

# **Authentication System**

### **General**

* Login + signup pages.  
* Protected dashboard only accessible after login.  
* Store **users** in `users.json`
* Store **sessions** in `sessions.json`
* Use HTTP-only cookies to store `sessionId`
* Update JSON dynamically for CRUD operations.  

## **Login Page Requirements**

* Must include Fields:

  * Username/email
  * Password
  * **Login** button
  * **Demo** button (auto-login using seeded admin)
* On login:

  * Validate credentials → Read the matching user from **`users.json`**
  * If valid, create a new session entry in **`sessions.json`**
  * Set cookie with `sessionId`
  * Redirect to the protected dashboard
* Invalid credentials must show a clear UI error state.

---

#### Signup Page Requirements

* Must include:

  * Name
  * Email
  * username
  * Password
  * Confirm password
  * Signup button
* On signup:

* Validate the payload
* Assign default role `"standard"`
* Add a new user entry to **`users.json`** under `"users"` array
* Generate unique `id`
* Must not overwrite seeded accounts

---

# Session Handling (`/data/sessions.json`)

Sessions must be stored **separately** from users.

### Required Structure

```json
{
  "sessions": [
    {
      "sessionId": "example-session-id-123",
      "userId": "user1",
      "createdAt": "2025-11-17T10:00:00Z",
      "demo": false
    }
  ]
}
```
### On Login

* Append new session
* Set cookie

### On Logout

* Remove session by `sessionId`

### Demo Session

* When the **Demo** button is clicked:

  * Auto-authenticate using the admin user in `users.json`
  * Create a session inside `sessions.json` with `"demo": true`
  * Redirect to dashboard

---

# **Protected Routes**

* Dashboard + internal pages require valid session
* Validate via cookie → check `sessions.json`
* Missing/invalid session 

---

# **Server & Deployment Configuration**

### **CRITICAL REQUIREMENT: Single Port Deployment**

The entire application MUST run on **port 3031** with the following architecture:

1. **Express Server Setup** (`server/server.ts`):
   * Listen on port **3031**
   * Serve built React frontend as static files
   * Handle API routes under `/api/*` prefix
   * Fallback to `index.html` for client-side routing (SPA)

2. **Vite Configuration** (`vite.config.ts`):
   * Build output directory: `dist/client`
   * Configure proxy for development only (not production)
   * Production build serves through Express

3. **API Route Structure**:
   * All backend routes MUST be prefixed with `/api/`
   * Examples: `/api/auth/login`, `/api/users/profile`, `/api/auth/logout`
   * Frontend calls APIs using relative paths: `/api/*`

4. **Static File Serving**:
   ```typescript
   // In server.ts
   app.use(express.static(path.join(__dirname, '../client')));
   app.get('*', (req, res) => {
     res.sendFile(path.join(__dirname, '../client/index.html'));
   });
   ```

5. **Package.json Scripts**:
   * `dev`: Run both frontend and backend on the same port 3031 (dev mode)
   * `build`: Build frontend with Vite, compile backend TypeScript
   * `start`: Run production server on port 3031

**No separate frontend/backend ports in production. Everything on 3031.**

---

### **Documentation Organization**

All documentation files MUST be placed in the `/docs/` folder, including:
- `docs/PROJECT_STATUS.md` - Implementation status with timestamp (REQUIRED)
**EXCEPTION**: Only `README.md` remains at the root level for GitHub visibility.

## **Implementation Status Tracking**

### **REQUIRED: PROJECT_STATUS.md in /docs/ folder**

After creating the codebase, you MUST generate a `docs/PROJECT_STATUS.md` file with the following:

1. **Timestamp**: ISO 8601 format showing when the implementation was completed
2. **Implementation Status**: Checklist of all features and components
3. **Completed Features**: List all implemented features with ✅
4. **Pending Items**: List any incomplete or future work with ❌
5. **Known Issues**: Document any limitations or bugs
6. **Testing Status**: Current state of tests (if any)

**Example Structure**:

```markdown
# Project Status

**Last Updated**: 2025-11-17T19:45:00Z

## Implementation Status

### ✅ Completed
- [x] Project structure setup
- [x] Frontend (React + TypeScript + Vite)
- [x] Backend (Express + TypeScript)
- [x] Authentication system (login/signup/logout)
- [x] Session management
- [x] User profile feature
- [x] Landing page
- [x] Dashboard
- [x] Theme toggle (light/dark)
- [x] File-based storage (users.json, sessions.json)
- [x] User seeding

### ❌ Pending
- [ ] Unit tests
- [ ] E2E tests
- [ ] Production deployment scripts

## Known Issues
- None at this time

## Notes
- Application runs on port 3031
- Uses JSON files for data storage (prototype only)
```

This file MUST be created in the `/docs/` folder immediately after the codebase is generated to provide clear visibility of what has been implemented.

---

# Output Format

Deliver a **production-grade, scalable monorepo** with modular feature folders, JSON-based storage, authentication, session handling, and a visually polished dashboard + landing page, using React + Express fully aligned with the best practices. The entire application MUST run on a single port (3031) with Express serving both the API and the built frontend.

---
