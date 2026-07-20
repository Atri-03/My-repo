import { useQuery } from '@tanstack/react-query';
import { Card } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { auditLogEntriesApi } from '../api/auditService';
import type { AuditLogEntry } from '../api/types';

const columns: DataTableColumn<AuditLogEntry>[] = [
  { key: 'id', label: 'ID', render: (a) => a.id },
  { key: 'entity_type', label: 'Entity Type', render: (a) => a.entity_type },
  { key: 'entity_id', label: 'Entity ID', render: (a) => a.entity_id },
  { key: 'action', label: 'Action', render: (a) => a.action },
  { key: 'actor', label: 'Actor', render: (a) => a.actor },
  {
    key: 'occurred_at',
    label: 'Occurred At',
    render: (a) => (a.occurred_at ? new Date(a.occurred_at).toLocaleString() : '—'),
  },
];

/** Audit Dashboard page: chronological audit log entries from the Audit Service. */
export function AuditDashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['audit-log-entries'],
    queryFn: () => auditLogEntriesApi.list(),
  });

  return (
    <div>
      <PageHeader
        title="Audit Dashboard"
        description="Immutable audit trail of create/update/delete actions across the platform."
      />
      <Card>
        <DataTable
          items={data ?? []}
          columns={columns}
          getRowId={(a) => a.id}
          isLoading={isLoading}
          error={error}
          emptyMessage="No audit log entries found."
        />
      </Card>
    </div>
  );
}
