# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is CORE-SE, a full-stack engineering workspace application that aggregates data from multiple external systems (JAMA, JIRA, Windchill, Outlook) into a unified interface. The application consists of:

- **Frontend**: Next.js 15 with React 19, TypeScript, and Tailwind CSS
- **Backend**: Python FastAPI with SQLAlchemy, SQLite database, and external system integrations
- **FDS Service**: A separate fake data service for demo purposes

## Development Commands

### Full Stack Development

**Start both frontend and backend together:**
```bash
# Windows batch script (recommended)
start.bat

# Manual startup (if batch fails):
# Terminal 1 - Backend
cd backend
python start_backend.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

**Note**: The system includes a rule to NOT automatically start servers. Always ask before starting servers unless specifically requested.

### Frontend Commands

```bash
cd frontend

# Development
npm run dev          # Start Next.js dev server (uses Turbo)
npm run build        # Build for production
npm start           # Start production server
npm run lint        # Run ESLint

# Dependencies
npm install --legacy-peer-deps    # Install dependencies (required flag)
```

### Backend Commands

```bash
cd backend

# Development (activate virtual env first)
core_env\Scripts\activate.bat    # Windows
python start_backend.py          # Start FastAPI server
python main.py                   # Alternative startup

# Testing
python test_apis.py             # Run API tests

# Database
# Uses SQLite by default (core_demo.db)
# Alembic for migrations (configured but basic setup)
```

## Architecture Overview

### Frontend Architecture

The frontend follows Next.js App Router structure:

- **`src/app/`**: Main application with layout.tsx and page.tsx
- **`src/components/`**: Reusable UI components including specialized sections:
  - `PulseSection` - Activity feed aggregation
  - `TasksSection` - Task management
  - `NotesSection` - Engineering notes with markdown support
  - `TraceImpactSection` - Requirements traceability analysis
  - `KnowledgeAgentsSection` - AI-powered knowledge base
  - `ToolWindowSection` - External system integrations
- **`src/hooks/`**: Custom React hooks including theme management
- **`src/lib/`**: Utility functions and shared logic

**Key Technologies:**
- Radix UI components with custom styling
- Framer Motion for animations
- React Hook Form with Zod validation
- Tailwind CSS with custom theme system
- Three.js integration (@react-three/fiber, @react-three/drei)

### Backend Architecture

The backend uses a modular FastAPI structure:

- **`app/routers/`**: API route modules by feature:
  - `pulse.py` - Aggregated activity feed from all systems
  - `tasks.py` - Task/work item management
  - `notes.py` - Engineering notes with citations
  - `impact.py` - Impact analysis and traceability
  - `knowledge.py` - Knowledge base and search
  - `ai.py` - AI/LLM operations (OpenAI integration)
  - `windows.py` - External system window management
  - `config.py` - Application configuration
- **`app/models.py`**: Comprehensive Pydantic models for all entities
- **`app/database.py`**: SQLAlchemy setup with SQLite
- **`app/config.py`**: Settings with environment variable support

**Key Integrations:**
- External systems via HTTP calls to FDS service
- OpenAI API for AI features (summaries, subtasks, analysis)
- SQLite database for local data storage
- CORS configured for frontend development

### External Systems Integration

The application integrates with several external engineering systems through a Fake Data Service (FDS):

- **JAMA**: Requirements management
- **JIRA**: Issue tracking  
- **Windchill**: CAD/PLM system
- **Outlook**: Email integration

All external calls are routed through the FDS service running on port 8001, which provides mock data that simulates real system responses.

## Development Workflow

### Running Tests

```bash
# Backend API tests
cd backend
python test_apis.py

# Frontend has ESLint configured but no test framework setup
cd frontend  
npm run lint
```

### Database Operations

The application uses SQLite with Alembic for migrations:

```bash
cd backend
# Database file: core_demo.db
# Models defined in app/models.py
# Basic migration setup present but minimal
```

### Environment Configuration

Backend uses `.env` file with settings like:
- `MODE=demo` - Application mode
- `FDS_BASE_URL=http://localhost:8001` - Fake data service
- `OPENAI_API_KEY` - For AI features
- Feature flags for different capabilities

## Code Patterns

### Frontend Patterns
- Custom theme system with CSS variables
- Component composition with Radix UI primitives
- State management through React hooks and context
- Mock data generation functions for development

### Backend Patterns  
- Pydantic models for request/response validation
- Dependency injection for authentication and settings
- Async/await for external HTTP calls
- Structured error handling with custom exceptions

### API Communication
- RESTful endpoints with `/api` prefix
- Standardized artifact reference system across all external systems
- Comprehensive error responses with proper HTTP status codes

## Important Notes

- The application is designed as a demo/prototype system
- Uses mock data through the FDS service rather than real external system connections
- Authentication is simplified for demo purposes (demo token: "demo-token-123")
- Database is SQLite-based for simplicity
- Frontend includes extensive UI component library with animations and 3D elements
- Backend provides comprehensive API for all frontend features

## AI/LLM Integration

The system includes built-in AI capabilities:
- Text summarization
- Subtask generation  
- Bullet point creation
- Knowledge base search and retrieval
- Daily report generation

AI features require OpenAI API key configuration and can be toggled via feature flags.