import { useQuery } from '@tanstack/react-query';
import { Card } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { StatusBadge } from '../components/StatusBadge';
import { mcpGatewayApi, type ActiveWorkflowRun } from '../api/mcpGatewayService';

const columns: DataTableColumn<ActiveWorkflowRun>[] = [
  { key: 'id', label: 'Run ID', render: (r) => r.id },
  { key: 'current_state', label: 'Current Agent State', render: (r) => <StatusBadge status={r.current_state} /> },
  {
    key: 'started_at',
    label: 'Started',
    render: (r) => (r.started_at ? new Date(r.started_at).toLocaleString() : '—'),
  },
];

/**
 * Agent Monitor page: shows currently active LangGraph agent pipeline runs
 * (transcript ingest -> requirement extraction -> FS/TS generation -> human gates)
 * via the MCP Gateway's `list_active_runs` tool.
 */
export function AgentMonitorPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['mcp-active-runs'],
    queryFn: () => mcpGatewayApi.listActiveRuns(),
    refetchInterval: 15000,
  });

  return (
    <div>
      <PageHeader
        title="Agent Monitor"
        description="Live view of active ABAP RAG pipeline agent runs, proxied through the MCP Gateway."
      />
      <Card>
        <DataTable
          items={data ?? []}
          columns={columns}
          getRowId={(r) => r.id}
          isLoading={isLoading}
          error={error}
          emptyMessage="No active agent runs at the moment."
        />
      </Card>
    </div>
  );
}
