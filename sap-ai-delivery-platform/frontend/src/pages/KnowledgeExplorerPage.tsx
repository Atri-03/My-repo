import { useQuery } from '@tanstack/react-query';
import { Card, Badge } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { knowledgeChunksApi, knowledgeSourcesApi } from '../api/ragService';
import type { KnowledgeChunk, KnowledgeSource } from '../api/types';

const sourceColumns: DataTableColumn<KnowledgeSource>[] = [
  { key: 'id', label: 'ID', render: (s) => s.id },
  { key: 'source_type', label: 'Type', render: (s) => s.source_type },
  { key: 'uri', label: 'URI', render: (s) => s.uri },
  {
    key: 'is_dead_link',
    label: 'Link Status',
    render: (s) => <Badge color={s.is_dead_link ? 'danger' : 'success'}>{s.is_dead_link ? 'Dead' : 'Live'}</Badge>,
  },
  {
    key: 'last_indexed_at',
    label: 'Last Indexed',
    render: (s) => (s.last_indexed_at ? new Date(s.last_indexed_at).toLocaleString() : '—'),
  },
];

const chunkColumns: DataTableColumn<KnowledgeChunk>[] = [
  { key: 'id', label: 'ID', render: (c) => c.id },
  { key: 'knowledge_source_id', label: 'Source', render: (c) => c.knowledge_source_id },
  { key: 'chunk_index', label: 'Index', render: (c) => String(c.chunk_index) },
  { key: 'text', label: 'Text', render: (c) => c.text },
];

/** Knowledge Explorer page: indexed knowledge sources and their chunks in the RAG Service. */
export function KnowledgeExplorerPage() {
  const sourcesQuery = useQuery({
    queryKey: ['knowledge-sources'],
    queryFn: () => knowledgeSourcesApi.list(),
  });

  const chunksQuery = useQuery({
    queryKey: ['knowledge-chunks'],
    queryFn: () => knowledgeChunksApi.list(),
  });

  return (
    <div>
      <PageHeader
        title="Knowledge Explorer"
        description="Browse knowledge sources and their indexed chunks in the RAG Service."
      />
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={sourcesQuery.data ?? []}
          columns={sourceColumns}
          getRowId={(s) => s.id}
          isLoading={sourcesQuery.isLoading}
          error={sourcesQuery.error}
          emptyMessage="No knowledge sources found."
        />
      </Card>
      <Card>
        <DataTable
          items={chunksQuery.data ?? []}
          columns={chunkColumns}
          getRowId={(c) => c.id}
          isLoading={chunksQuery.isLoading}
          error={chunksQuery.error}
          emptyMessage="No knowledge chunks found."
        />
      </Card>
    </div>
  );
}
