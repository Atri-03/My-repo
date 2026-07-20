/**
 * Base URLs for every backend microservice, resolved from Vite environment
 * variables with sensible localhost defaults matching docker-compose.yml.
 */
export const serviceBaseUrls = {
  transcript: import.meta.env.VITE_TRANSCRIPT_SERVICE_URL ?? 'http://localhost:8001/api/v1',
  documentExtraction:
    import.meta.env.VITE_DOCUMENT_EXTRACTION_SERVICE_URL ?? 'http://localhost:8002/api/v1',
  fs: import.meta.env.VITE_FS_SERVICE_URL ?? 'http://localhost:8003/api/v1',
  ts: import.meta.env.VITE_TS_SERVICE_URL ?? 'http://localhost:8004/api/v1',
  review: import.meta.env.VITE_REVIEW_SERVICE_URL ?? 'http://localhost:8005/api/v1',
  approval: import.meta.env.VITE_APPROVAL_SERVICE_URL ?? 'http://localhost:8006/api/v1',
  audit: import.meta.env.VITE_AUDIT_SERVICE_URL ?? 'http://localhost:8007/api/v1',
  rag: import.meta.env.VITE_RAG_SERVICE_URL ?? 'http://localhost:8008/api/v1',
  user: import.meta.env.VITE_USER_SERVICE_URL ?? 'http://localhost:8009/api/v1',
  workflow: import.meta.env.VITE_WORKFLOW_SERVICE_URL ?? 'http://localhost:8010/api/v1',
  mcpGateway: import.meta.env.VITE_MCP_GATEWAY_SERVICE_URL ?? 'http://localhost:8011/api/v1',
  sapExecution: import.meta.env.VITE_SAP_EXECUTION_SERVICE_URL ?? 'http://localhost:8100/api/v1',
} as const;

export type ServiceName = keyof typeof serviceBaseUrls;
