/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_TRANSCRIPT_SERVICE_URL?: string;
  readonly VITE_DOCUMENT_EXTRACTION_SERVICE_URL?: string;
  readonly VITE_FS_SERVICE_URL?: string;
  readonly VITE_TS_SERVICE_URL?: string;
  readonly VITE_REVIEW_SERVICE_URL?: string;
  readonly VITE_APPROVAL_SERVICE_URL?: string;
  readonly VITE_AUDIT_SERVICE_URL?: string;
  readonly VITE_RAG_SERVICE_URL?: string;
  readonly VITE_USER_SERVICE_URL?: string;
  readonly VITE_WORKFLOW_SERVICE_URL?: string;
  readonly VITE_MCP_GATEWAY_SERVICE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
