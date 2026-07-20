import { resourceClient } from './client';
import type { AuditLogEntry } from './types';

export const auditLogEntriesApi = resourceClient<AuditLogEntry>('audit', '/audit-log-entries');
