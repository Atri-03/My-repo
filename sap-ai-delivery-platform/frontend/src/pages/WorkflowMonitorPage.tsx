import { useQuery } from '@tanstack/react-query';
import { Card } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { StatusBadge } from '../components/StatusBadge';
import { workflowEventsApi, workflowRunsApi } from '../api/workflowService';
import type { WorkflowEvent, WorkflowRun } from '../api/types';

const runColumns: DataTableColumn<WorkflowRun>[] = [
  { key: 'id', label: 'ID', render: (r) => r.id },
  { key: 'transcript_id', label: 'Transcript', render: (r) => r.transcript_id },
  { key: 'current_state', label: 'State', render: (r) => <StatusBadge status={r.current_state} /> },
  { key: 'started_at', label: 'Started', render: (r) => (r.started_at ? new Date(r.started_at).toLocaleString() : '—') },
  {
    key: 'completed_at',
    label: 'Completed',
    render: (r) => (r.completed_at ? new Date(r.completed_at).toLocaleString() : '—'),
  },
];

const eventColumns: DataTableColumn<WorkflowEvent>[] = [
  { key: 'id', label: 'ID', render: (e) => e.id },
  { key: 'workflow_run_id', label: 'Run', render: (e) => e.workflow_run_id },
  { key: 'from_state', label: 'From', render: (e) => e.from_state ?? '—' },
  { key: 'to_state', label: 'To', render: (e) => e.to_state },
  { key: 'actor', label: 'Actor', render: (e) => e.actor },
  {
    key: 'occurred_at',
    label: 'Occurred',
    render: (e) => (e.occurred_at ? new Date(e.occurred_at).toLocaleString() : '—'),
  },
];

/** Workflow Monitor page: LangGraph pipeline workflow runs and their state transitions. */
export function WorkflowMonitorPage() {
  const runsQuery = useQuery({
    queryKey: ['workflow-runs'],
    queryFn: () => workflowRunsApi.list(),
  });

  const eventsQuery = useQuery({
    queryKey: ['workflow-events'],
    queryFn: () => workflowEventsApi.list(),
  });

  return (
    <div>
      <PageHeader
        title="Workflow Monitor"
        description="End-to-end workflow runs (transcript to SAP execution package) and their state events."
      />
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={runsQuery.data ?? []}
          columns={runColumns}
          getRowId={(r) => r.id}
          isLoading={runsQuery.isLoading}
          error={runsQuery.error}
          emptyMessage="No workflow runs found."
        />
      </Card>
      <Card>
        <DataTable
          items={eventsQuery.data ?? []}
          columns={eventColumns}
          getRowId={(e) => e.id}
          isLoading={eventsQuery.isLoading}
          error={eventsQuery.error}
          emptyMessage="No workflow events found."
        />
      </Card>
    </div>
  );
}
