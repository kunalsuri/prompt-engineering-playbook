---
mode: 'agent'
description: 'Generate a comprehensive Test Suite for My-SAAS-APP (React/Vitest + FastAPI/Pytest)'
version: '1.0.0'
---

> **Learn why this works:** [Constrained Output + Evaluation](../../../learn/03-patterns.md#36-pattern-5-constrained-output)

# Role
Act as a **Software Development Engineer in Test (SDET)** and **QA Architect**.
Your goal is to set up a robust, automated testing infrastructure for the **My-SAAS-APP** monorepo.

# Task

# 🛡️ Testing Philosophy
1.  **Backend (FastAPI)**: Focus on **Integration Tests** (API endpoints) and **Unit Tests** (Service logic).
    * **CRITICAL**: You MUST mock the `JsonStore` file I/O in `conftest.py`. Tests must **never** read/write to the real `backend/data/` folder.
    * Use the `tmp_path` fixture for all file operations.
2.  **Frontend (React)**: Focus on **Behavioral Testing**.
    * Test what the user *sees* and *does* (e.g., "User clicks login"), not implementation details.
    * Mock all network requests at the `api` module level.

# 📊 Coverage & Quality Targets
* **Backend**: 80%+ overall coverage.
* **Frontend**: Focus on critical user flows (Login, Profile Update).
* **Tools**: `pytest-cov` (backend), `vitest --coverage` (frontend).

---

# ⚙️ Tech Stack & Tools

### Backend
* **Framework**: `pytest`
* **Async Support**: `pytest-asyncio`
* **Requests**: `httpx` (for `AsyncClient`)
* **Mocking**: `pytest-mock`
* **Coverage**: `pytest-cov`

### Frontend
* **Runner**: `vitest` (Native Vite integration)
* **Environment**: `jsdom`
* **Utilities**: `@testing-library/react`, `@testing-library/user-event`, `@testing-library/jest-dom`

---

# 📋 Execution Plan

## Phase 1: Backend Testing Infrastructure (`/backend`)

1.  **Install Dependencies**:
    `pip install pytest pytest-asyncio httpx pytest-mock pytest-cov`

2.  **Configuration**:
    * Create `pytest.ini`: Configure python paths, async mode (`asyncio_mode = auto`), and coverage settings.

3.  **Fixtures (`tests/conftest.py`)**:
    * **Mock Data Store**:
        ```python
        @pytest.fixture(autouse=True)
        def mock_json_store(tmp_path, monkeypatch):
            # Override the class variable or init path to use tmp_path
            monkeypatch.setattr('app.db.json_store.JsonStore.DATA_DIR', tmp_path)
        ```
    * **Async Client**: Yield an `httpx.AsyncClient` connected to `app`.

4.  **Test Cases (`tests/api/`)**:
    * `test_auth.py`: Signup success, Duplicate email error, Login success, Invalid creds.
    * `test_users.py`: Get profile (auth vs unauth), Update profile.
    * `test_json_store.py`: Unit test the atomic write/lock logic (using tmp files).

## Phase 2: Frontend Testing Infrastructure (`/frontend`)

1.  **Install Dependencies**:
    `npm install -D vitest jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom @vitest/coverage-v8`

2.  **Configuration**:
    * Update `vite.config.ts`: Add `test` object (`globals: true`, `environment: 'jsdom'`, `setupFiles: './src/test/setup.ts'`).
    * Create `src/test/setup.ts`: Import `@testing-library/jest-dom`.

3.  **Test Cases**:
    * **Unit**: `lib/utils.test.ts` (Tailwind class merger).
    * **Component**: `components/ui/button.test.tsx` (Variant rendering).
    * **Feature**: `features/auth/components/LoginForm.test.tsx`:
        * Mock `api.login` using `vi.spyOn`.
        * Test: Renders form -> Validates inputs -> Calls API on submit -> Handles Error/Success.

---

# 📝 Test Naming Standards

* **Backend**: `def test_<feature>_<scenario>_<expected_result>():`
    * Example: `test_login_with_invalid_password_returns_401`
* **Frontend**: `it('should <expected behavior> when <condition>')`
    * Example: `it('should display error message when login fails')`

---

# Output Format

### 1. Backend Code
* `backend/pytest.ini`
* `backend/tests/conftest.py` (**MUST** include `mock_json_store` and `client` fixtures).
* `backend/tests/api/test_auth.py` (At least 3 scenarios).

### 2. Frontend Code
* `frontend/vite.config.ts` (The `test` config block).
* `frontend/src/test/setup.ts`.
* `frontend/src/features/auth/components/LoginForm.test.tsx` (Full behavioral test).

---

# 🚨 Critical Constraints

1.  **Isolation**: Backend tests must NEVER touch `backend/data/users.json`. Use `tmp_path`.
2.  **Async**: All FastAPI tests must be `async def`.
3.  **Mocking**: Frontend tests must mock the API layer. Do not rely on a running backend.
4.  **Completeness**: Ensure all imports are present. Do not use `...` for boilerplate.

---

# 🏁 Action
Generate the code following the **Execution Plan** order. Start with Phase 1 (Backend).