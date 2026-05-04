# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.
Also contains a standalone Python + Streamlit app (`ai-interview-simulator/`).

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## AI Interview Simulator (`ai-interview-simulator/`)

A standalone Python + Streamlit app.

- **Language**: Python 3.11
- **UI**: Streamlit (port 5000)
- **AI**: OpenAI GPT via Replit AI Integrations proxy
- **Charts**: Plotly
- **Run**: `cd ai-interview-simulator && streamlit run app.py --server.port 5000`

### Module structure

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit app (3 tabs: Interview, Results, Dashboard) |
| `modules/config.py` | Roles, difficulty levels, constants |
| `modules/session_manager.py` | Session state management |
| `modules/question_generator.py` | OpenAI question generation |
| `modules/answer_evaluator.py` | OpenAI answer evaluation & scoring |
| `modules/dashboard.py` | Plotly chart rendering |

### AI Integration

Uses `AI_INTEGRATIONS_OPENAI_BASE_URL` and `AI_INTEGRATIONS_OPENAI_API_KEY` env vars
(auto-provisioned by Replit AI Integrations — no manual key needed on Replit).

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.
