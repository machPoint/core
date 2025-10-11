# CORE-SE Demo PRD (Full Document)

> **Context:** Demo build only. Frontend is **Node/React**; backend is **Python FastAPI**. No live Jama/Jira/Windchill/Email/Outlook/OPAL yet—use a **Fake Data Service** (FDS) behind the backend. For AI microcalls (summaries, subtasks, bullets, daily reports), use **OpenAI Chat API** via backend.
>
> **Goal:** Deliver a click-through demo that matches the screenshot UI: Notes-first, Pulse/Impact awareness, read-only windows, Tasks, Knowledge, Themes, Outlook integration. Demo must be upgradeable to MVP later without major rewrites.

---

## A) Frontend PRD (Node/React)

### A1. Objectives
- Present a **notes-first workspace** with left navigation: 
  1. Notes  
  2. Pulse  
  3. Requirements  
  4. Design & Interfaces  
  5. Verification  
  6. Trace Graph  
  7. Impact Analysis  
  8. Knowledge  
  9. Tasks  
  10. Agents  
  11. Admin  
  12. Themes
- Provide **quick actions** in the right context panel: Open in Source, Save to Note, Add to Task, Summarize, Break into Subtasks, Daily Report.
- Render **read-only windows** for Jama/Jira/Windchill/Outlook mock detail pages.
- Stream responses from AI microcalls; never expose OpenAI keys to browser.
- Provide **Themes** to switch appearance (dark, light, custom palettes) to match engineering preferences.

### A2. Tech & Structure
- **React 18+** with **TypeScript**.
- **Router**: file-based (Next.js) or React Router.
- **State**: RTK Query/Zustand for server cache; local editor state for notes.
- **Styling**: Tailwind + shadcn/ui in dark mode by default; theme switcher with persistent preference.
- **Icons**: lucide-react.
- **Charts/Graph**: Recharts + vis-network or Cytoscape.js for Trace Graph.
- **Transport**: REST + SSE for AI microcalls.

### A3. Pages & Key Components
1. **Notes**
   - `NotesList` (search, tags, folders) → `NoteEditor` (markdown) → `RightPanel`.
   - Inline **ArtifactChip** rendering `@REQ-123` or `@OUTLOOK-MSG-001` with status and source.
   - Actions: Convert selection → Task, Summarize selection, Make subtasks.

2. **Pulse**
   - `PulseFeed` grouped by day; filters (source/type: Jama, Jira, Windchill, Outlook, Email).
   - Item actions: Open Impact, Open in Source, Save to Note, Add to Task, Summarize, Subtasks.

3. **Requirements / Design & Interfaces / Verification**
   - `WindowFrame` with Read-Only watermark loads backend-resolved links (mock Jama/Jira/Windchill pages).

4. **Trace Graph**
   - `TraceCanvas` with node types (Requirement, Test, Issue, Part, BOM, ECN, Outlook Message).
   - Controls: search, focus path, highlight gaps, export PNG.

5. **Impact Analysis**
   - `ImpactInput` (search/paste ID) → `ImpactTree` + `ImpactTable`.
   - Actions: Add to Task, Save to Note, Open in Source.

6. **Knowledge**
   - `KnowledgeSearch` → result cards with drag-to-cite into Notes.

7. **Tasks**
   - `TaskList` (title, status, due, owner, context) + `TaskDetail` (linked artifacts, generated subtasks).

8. **Agents**
   - Cards to trigger backend jobs (Trace Audit, Impact, Verification Planner, Daily Summary). Demo can stub outputs.

9. **Admin**
   - Toggle features, show connector states (all demo), view audit log stubs.

10. **Themes**
    - UI toggle for dark/light/custom.
    - Theme persistence in local storage.

11. **Right Context Panel** (global)
    - Related items (reqs/tests/parts/issues/messages).
    - AI insights (coverage %, risk).
    - Quick Actions: Open in Source, Save to Note, Add to Task, Summarize, Subtasks, Daily Summary.

### A4. Frontend → Backend Contracts
- `/pulse`, `/impact/{id}`, `/tasks`, `/notes`, `/windows/{tool}/{id}`, `/knowledge`, `/ai/summarize`, `/ai/subtasks`, `/ai/bullets`, `/ai/daily_report`, `/config`.
- Never call OpenAI from the browser.

### A5. Feature Flags (read from `/config`)
- `FEATURE_EMAIL`, `FEATURE_WINDCHILL`, `FEATURE_OUTLOOK`, `FEATURE_AI_MICROCALLS`, `FEATURE_TRACE_GRAPH`, `FEATURE_THEMES`.

### A6. Acceptance (Frontend)
- Notes render artifacts from all sources (including Outlook messages).
- Pulse shows changes from Jama/Jira/Windchill/Outlook/Email.
- Tasks can be created from Pulse/Impact/Notes.
- Daily summary button triggers AI endpoint.
- Theme switcher works across app.

---

## B) Backend PRD (Python FastAPI)

### B1. Objectives
- Act as **single API** for the React app.
- Proxy to Fake Data Service for Jama/Jira/Windchill/Email/Outlook.
- Provide AI microcalls using OpenAI Chat API (summaries, subtasks, bullets, daily summary reports).
- Manage Tasks and Notes locally.
- Return deep links for read-only windows.

### B2. Services
- **API Gateway (FastAPI)** with CORS and demo token auth.
- **FDS client** to `/mock/*` routes.
- **AI client** to OpenAI (fast model; JSON mode).
- **Task Service** (SQLite → Postgres later).
- **Report Service** for daily summaries (compiles Pulse + Tasks).

### B3. Endpoints & Schemas
1. **Pulse**
   - `GET /pulse?since&sources&types&limit` → includes Outlook.
2. **Impact**
   - `GET /impact/{entityId}?depth=2` → ripple tree + table.
3. **Tasks**
   - `GET /tasks`, `POST /tasks`, `PATCH /tasks/{id}`.
4. **Notes**
   - `POST /notes` {title, body, citations[]}.
5. **Knowledge**
   - `GET /knowledge?q=&limit=`.
6. **Windows**
   - `GET /windows/{tool}/{id}` → deep links for Jama/Jira/Windchill/Outlook.
7. **AI microcalls**
   - `POST /ai/summarize`, `/ai/subtasks`, `/ai/bullets`, `/ai/daily_report`.
8. **Config**
   - `GET /config` → feature flags, theme list.

**Example Daily Report response:**
```json
{"report":"Daily summary: 5 changes detected (3 Jama, 1 Jira, 1 Outlook). 2 new tasks created. Coverage gaps remain at 22%."}
```

### B4. Fake Data Service Additions
- `/mock/outlook/messages?since=...` (subject, sender, date, linked artifacts).
- Pulse aggregator merges Outlook events into feed.

### B5. Themes
- Backend `/config` returns `themes:[dark,light,custom]`.

### B6. Acceptance (Backend)
- `/pulse` includes Outlook and Email events.
- `/ai/daily_report` produces usable plain summary.
- `/windows/outlook/{id}` resolves mock Outlook message.
- `/config` lists theme options.

---

## C) Fake Data Service PRD

### C1. Objective
Provide a mock service simulating Jama, Jira, Windchill, Email, Outlook for demo development.

### C2. Endpoints
- `/mock/jama/items`, `/mock/jama/relationships`, `/mock/jama/baselines`
- `/mock/jira/issues`, `/mock/jira/links`
- `/mock/windchill/parts`, `/mock/windchill/bom`, `/mock/windchill/ecn`
- `/mock/email/messages`, `/mock/outlook/messages`
- `/mock/graph/trace`, `/mock/impact/{id}`, `/mock/pulse`
- `/mock/admin/seed`

### C3. Data Fixtures
- 100 requirements, 50 tests, 30 issues, 20 parts, 5 ECNs, 10 emails, 10 outlook messages.
- Pre-linked with ~15% gaps.
- Baseline snapshots for diffs.
- Tasks seeded with open/closed examples.

### C4. Change Simulator
- Events: requirement text change, relationship change, ECN raised/approved, Jira issue created/closed, Outlook/email event.
- Emits Pulse items; can POST to backend webhook.

### C5. Acceptance
- Frontend renders all tabs using only mock data.
- Pulse & Impact show events across Jama/Jira/Windchill/Email/Outlook.
- Tasks can be created from Pulse.
- Windows links open mock HTML pages with watermark.

---

## D) Demo Runbook
1. Seed mock dataset.
2. Open Notes; embed `@OUTLOOK-MSG-001` chip.
3. Pulse shows Outlook message about ECN approval.
4. Run Impact Analysis on REQ-123 → ripple includes linked artifacts.
5. Add to Task List; open Tasks; generate subtasks via AI.
6. Trigger Daily Report → AI endpoint returns summary.
7. Switch Theme from dark → light → custom.

---

## E) Extensibility to MVP
- Replace Outlook FDS with real Microsoft Graph API connector.
- Daily summaries delivered by email via Outlook.
- Replace OpenAI API calls with SLIMs service.
- SQLite → Postgres, in-memory cache → Redis.
- RBAC, OIDC auth, multi-project workspaces.

---

**This full PRD combines Frontend, Backend, and Fake Data specifications for the CORE-SE demo, with Outlook + Themes integration and Daily Summary reports.**

