export interface NavItem {
  path: string;
  label: string;
}

/** Ordered list of pages exposed via the main navigation. */
export const navItems: NavItem[] = [
  { path: '/', label: 'Dashboard' },
  { path: '/transcript-queue', label: 'Transcript Queue' },
  { path: '/requirement-view', label: 'Requirement View' },
  { path: '/fs-review', label: 'FS Review' },
  { path: '/ts-review', label: 'TS Review' },
  { path: '/rag-search', label: 'RAG Search' },
  { path: '/knowledge-explorer', label: 'Knowledge Explorer' },
  { path: '/audit-dashboard', label: 'Audit Dashboard' },
  { path: '/workflow-monitor', label: 'Workflow Monitor' },
  { path: '/agent-monitor', label: 'Agent Monitor' },
  { path: '/mcp-monitor', label: 'MCP Monitor' },
  { path: '/sap-execution', label: 'SAP Execution' },
  { path: '/configuration', label: 'Configuration' },
  { path: '/administration', label: 'Administration' },
];
