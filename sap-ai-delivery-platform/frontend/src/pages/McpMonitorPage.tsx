import { useQuery } from '@tanstack/react-query';
import { Badge, Card, Spinner, Text } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { getServiceHealth } from '../api/client';
import { mcpGatewayApi } from '../api/mcpGatewayService';

interface SourceRow {
  id: string;
  source_type: string;
  uri: string;
  is_dead_link: boolean;
}

const columns: DataTableColumn<SourceRow>[] = [
  { key: 'id', label: 'ID', render: (s) => s.id },
  { key: 'source_type', label: 'Type', render: (s) => s.source_type },
  { key: 'uri', label: 'URI', render: (s) => s.uri },
  {
    key: 'status',
    label: 'Status',
    render: (s) => <Badge color={s.is_dead_link ? 'danger' : 'success'}>{s.is_dead_link ? 'Dead' : 'Reachable'}</Badge>,
  },
];

/** MCP Monitor page: health of the MCP Gateway service and the knowledge sources it exposes as tools. */
export function McpMonitorPage() {
  const healthQuery = useQuery({
    queryKey: ['mcp-health'],
    queryFn: () => getServiceHealth('mcpGateway'),
    refetchInterval: 15000,
  });

  const sourcesQuery = useQuery({
    queryKey: ['mcp-list-sources'],
    queryFn: () => mcpGatewayApi.listSources(),
  });

  const sources = (sourcesQuery.data?.sources ?? []) as unknown as SourceRow[];

  return (
    <div>
      <PageHeader
        title="MCP Monitor"
        description="Health and tool availability of the MCP Gateway Service, which exposes platform capabilities as MCP tools."
      />
      <Card style={{ marginBottom: '16px', padding: '16px' }}>
        {healthQuery.isLoading && <Spinner label="Checking MCP Gateway health..." />}
        {healthQuery.error && (
          <Badge color="danger" appearance="filled">
            MCP Gateway unreachable
          </Badge>
        )}
        {healthQuery.data && (
          <Text>
            MCP Gateway status: <Badge color="success">{healthQuery.data.status}</Badge>
          </Text>
        )}
      </Card>
      <Card>
        <DataTable
          items={sources}
          columns={columns}
          getRowId={(s) => s.id}
          isLoading={sourcesQuery.isLoading}
          error={sourcesQuery.error}
          emptyMessage="No knowledge sources registered as MCP tools."
        />
      </Card>
    </div>
  );
}
