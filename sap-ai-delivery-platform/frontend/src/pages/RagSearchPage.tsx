import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Button, Card, Field, Input, Badge } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { mcpGatewayApi } from '../api/mcpGatewayService';
import type { SearchDocumentsResult } from '../api/types';

const columns: DataTableColumn<SearchDocumentsResult>[] = [
  { key: 'chunk_id', label: 'Chunk', render: (r) => r.chunk_id },
  { key: 'source_type', label: 'Source Type', render: (r) => r.source_type },
  { key: 'text', label: 'Text', render: (r) => r.text },
  { key: 'score', label: 'Score', render: (r) => r.score.toFixed(3) },
  {
    key: 'dead_link',
    label: 'Link Status',
    render: (r) => <Badge color={r.is_dead_link ? 'danger' : 'success'}>{r.is_dead_link ? 'Dead' : 'Live'}</Badge>,
  },
];

/** RAG Search page: hybrid search over indexed knowledge via the MCP Gateway. */
export function RagSearchPage() {
  const [query, setQuery] = useState('');
  const searchMutation = useMutation({
    mutationFn: () => mcpGatewayApi.searchDocuments({ query, top: 10, search_mode: 'hybrid' }),
  });

  const handleSearch = () => {
    if (query.trim().length > 0) {
      searchMutation.mutate();
    }
  };

  return (
    <div>
      <PageHeader
        title="RAG Search"
        description="Search indexed knowledge sources using the MCP Gateway's hybrid retrieval tool."
      />
      <Card style={{ marginBottom: '16px', padding: '16px' }}>
        <Field label="Search query">
          <Input
            value={query}
            onChange={(_e, data) => setQuery(data.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="e.g. sales order pricing procedure"
          />
        </Field>
        <Button appearance="primary" onClick={handleSearch} style={{ marginTop: '12px' }}>
          Search
        </Button>
      </Card>
      <Card>
        <DataTable
          items={searchMutation.data?.results ?? []}
          columns={columns}
          getRowId={(r) => r.chunk_id}
          isLoading={searchMutation.isPending}
          error={searchMutation.error}
          emptyMessage="Run a search to see results."
        />
      </Card>
    </div>
  );
}
