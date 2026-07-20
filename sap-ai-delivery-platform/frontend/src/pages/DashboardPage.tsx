import { useQuery } from '@tanstack/react-query';
import { Card, CardHeader, Text, Title1, Badge, Spinner } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { transcriptsApi } from '../api/transcriptService';
import { requirementSetsApi } from '../api/documentExtractionService';
import { functionalSpecificationsApi } from '../api/fsService';
import { technicalSpecificationsApi } from '../api/tsService';
import { workflowRunsApi } from '../api/workflowService';
import { auditLogEntriesApi } from '../api/auditService';
import { getServiceHealth } from '../api/client';
import type { ServiceName } from '../api/config';

const summaryCards: Array<{ key: string; label: string; queryFn: () => Promise<unknown[]> }> = [
  { key: 'transcripts', label: 'Transcripts', queryFn: () => transcriptsApi.list() },
  { key: 'requirement-sets', label: 'Requirement Sets', queryFn: () => requirementSetsApi.list() },
  { key: 'functional-specifications', label: 'Functional Specifications', queryFn: () => functionalSpecificationsApi.list() },
  { key: 'technical-specifications', label: 'Technical Specifications', queryFn: () => technicalSpecificationsApi.list() },
  { key: 'workflow-runs', label: 'Workflow Runs', queryFn: () => workflowRunsApi.list() },
  { key: 'audit-log-entries', label: 'Audit Log Entries', queryFn: () => auditLogEntriesApi.list() },
];

const monitoredServices: Array<{ service: ServiceName; label: string }> = [
  { service: 'transcript', label: 'Transcript Service' },
  { service: 'documentExtraction', label: 'Document Extraction Service' },
  { service: 'fs', label: 'FS Service' },
  { service: 'ts', label: 'TS Service' },
  { service: 'review', label: 'Review Service' },
  { service: 'approval', label: 'Approval Service' },
  { service: 'audit', label: 'Audit Service' },
  { service: 'rag', label: 'RAG Service' },
  { service: 'user', label: 'User Service' },
  { service: 'workflow', label: 'Workflow Service' },
  { service: 'mcpGateway', label: 'MCP Gateway Service' },
];

function SummaryCard({ label, queryFn, cardKey }: { label: string; queryFn: () => Promise<unknown[]>; cardKey: string }) {
  const { data, isLoading, error } = useQuery({ queryKey: ['dashboard-summary', cardKey], queryFn });
  return (
    <Card style={{ minWidth: '200px' }}>
      <CardHeader header={<Text weight="semibold">{label}</Text>} />
      {isLoading && <Spinner size="tiny" />}
      {error && <Badge color="danger">unavailable</Badge>}
      {!isLoading && !error && <Title1>{data?.length ?? 0}</Title1>}
    </Card>
  );
}

function ServiceHealthBadge({ service, label }: { service: ServiceName; label: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['service-health', service],
    queryFn: () => getServiceHealth(service),
    refetchInterval: 30000,
    retry: false,
  });
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0' }}>
      <Text>{label}</Text>
      {isLoading && <Spinner size="tiny" />}
      {error && <Badge color="danger">offline</Badge>}
      {data && <Badge color="success">{data.status}</Badge>}
    </div>
  );
}

/** Dashboard page: platform-wide summary counts and per-service health status. */
export function DashboardPage() {
  return (
    <div>
      <PageHeader
        title="Dashboard"
        description="Platform-wide overview of delivery artefacts and backend service health."
      />
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', marginBottom: '24px' }}>
        {summaryCards.map((card) => (
          <SummaryCard key={card.key} cardKey={card.key} label={card.label} queryFn={card.queryFn} />
        ))}
      </div>
      <Card style={{ padding: '16px', maxWidth: '480px' }}>
        <Text weight="semibold">Service Health</Text>
        {monitoredServices.map((s) => (
          <ServiceHealthBadge key={s.service} service={s.service} label={s.label} />
        ))}
      </Card>
    </div>
  );
}
