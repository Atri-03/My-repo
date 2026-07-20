import { useQuery } from '@tanstack/react-query';
import { Card } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { transcriptsApi } from '../api/transcriptService';
import type { Transcript } from '../api/types';

const columns: DataTableColumn<Transcript>[] = [
  { key: 'id', label: 'ID', render: (t) => t.id },
  { key: 'source', label: 'Source Document', render: (t) => t.source_document_id },
  { key: 'format', label: 'Format', render: (t) => t.parsed_format },
  {
    key: 'meeting_date',
    label: 'Meeting Date',
    render: (t) => (t.meeting_date ? new Date(t.meeting_date).toLocaleString() : '—'),
  },
  {
    key: 'participants',
    label: 'Participants',
    render: (t) => (t.participants && t.participants.length > 0 ? t.participants.join(', ') : '—'),
  },
  {
    key: 'created_at',
    label: 'Ingested',
    render: (t) => (t.created_at ? new Date(t.created_at).toLocaleString() : '—'),
  },
];

/** Transcript Queue page: lists ingested transcripts awaiting downstream processing. */
export function TranscriptQueuePage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['transcripts'],
    queryFn: () => transcriptsApi.list(),
  });

  return (
    <div>
      <PageHeader
        title="Transcript Queue"
        description="Ingested meeting transcripts and source documents from the Transcript Service."
      />
      <Card>
        <DataTable
          items={data ?? []}
          columns={columns}
          getRowId={(t) => t.id}
          isLoading={isLoading}
          error={error}
          emptyMessage="No transcripts have been ingested yet."
        />
      </Card>
    </div>
  );
}
