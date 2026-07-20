# SAP AI Delivery Platform — Frontend

Production-grade React + TypeScript single-page application, built with
[Vite](https://vite.dev), [Fluent UI v9](https://react.fluentui.dev/) and
[TanStack Query](https://tanstack.com/query/latest), that surfaces the
platform's backend microservices through 13 pages.

## Getting started

```bash
npm install
cp .env.example .env   # adjust service base URLs if not using the defaults
npm run dev
```

The dev server runs on `http://localhost:5173` by default. Backend services
must be reachable (either via `docker compose up` from the parent directory,
or by running each service locally) and must allow CORS from the frontend's
origin (already configured via each service's `cors_origins` setting).

## Scripts

| Script             | Description                              |
| ------------------- | ----------------------------------------- |
| `npm run dev`        | Start the Vite dev server                |
| `npm run build`      | Type-check and build for production      |
| `npm run preview`    | Preview the production build locally     |
| `npm run lint`       | Run `oxlint`                             |
| `npm run test`       | Run the Vitest test suite once           |
| `npm run test:watch` | Run Vitest in watch mode                 |

## Configuration

Every backend microservice base URL is configurable via a `VITE_*`
environment variable (see `.env.example`). Defaults match the ports used in
`../docker-compose.yml` for local development.

## Pages and backend mapping

| Page               | Backend service(s)                                                          |
| ------------------ | ---------------------------------------------------------------------------- |
| Dashboard           | All services (summary counts + `/health` checks)                            |
| Transcript Queue    | Transcript Service (`/transcripts`, `/source-documents`)                     |
| Requirement View    | Document Extraction Service (`/requirement-sets`, `/requirements`)          |
| FS Review           | FS Service (`/functional-specifications`) + Review Service (`/review-cycles`) |
| TS Review           | TS Service (`/technical-specifications`) + Review Service (`/review-cycles`) |
| RAG Search          | MCP Gateway Service (`/tools/search_documents`)                             |
| Knowledge Explorer  | RAG Service (`/knowledge-sources`, `/knowledge-chunks`)                      |
| Audit Dashboard     | Audit Service (`/audit-log-entries`)                                        |
| Workflow Monitor    | Workflow Service (`/workflow-runs`, `/workflow-events`)                     |
| Agent Monitor       | MCP Gateway Service (`/tools/list_active_runs`)                             |
| MCP Monitor         | MCP Gateway Service (`/health`, `/tools/list_sources`)                       |
| Configuration       | User Service (`/tenants`, `/projects`) + FS Service (`/document-templates`) |
| Administration      | User Service (`/users`) + Approval Service (`/review-decisions`, `/sap-execution-packages`) |

## Architecture

- `src/api/` — typed Axios clients per backend service, generated from the
  services' Pydantic schemas, plus a generic `resourceClient` for standard
  CRUD REST resources.
- `src/components/` — shared, reusable UI building blocks (navigation shell,
  data table, status badge, page header).
- `src/pages/` — one component per page, each wired to the relevant backend
  API(s) via TanStack Query.
- `src/test/` — Vitest setup, Mock Service Worker (MSW) handlers/fixtures and
  a `renderWithProviders` test helper.

## Testing

Tests use [Vitest](https://vitest.dev), [React Testing Library](https://testing-library.com/react)
and [MSW](https://mswjs.io) to mock backend HTTP responses, so the suite runs
without any running backend services.

```bash
npm run test
```
