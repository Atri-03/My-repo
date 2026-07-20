import { useQuery } from '@tanstack/react-query';
import { Card } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { StatusBadge } from '../components/StatusBadge';
import { technicalSpecificationsApi } from '../api/tsService';
import { reviewCyclesApi } from '../api/reviewService';
import type { ReviewCycle, TechnicalSpecification } from '../api/types';

const specColumns: DataTableColumn<TechnicalSpecification>[] = [
  { key: 'id', label: 'ID', render: (ts) => ts.id },
  {
    key: 'functional_specification_id',
    label: 'Functional Specification',
    render: (ts) => ts.functional_specification_id,
  },
  { key: 'version', label: 'Version', render: (ts) => String(ts.version ?? '—') },
  { key: 'status', label: 'Status', render: (ts) => <StatusBadge status={ts.status} /> },
  {
    key: 'regeneration_count',
    label: 'Regenerations',
    render: (ts) => String(ts.regeneration_count ?? 0),
  },
];

const reviewColumns: DataTableColumn<ReviewCycle>[] = [
  { key: 'id', label: 'ID', render: (r) => r.id },
  { key: 'artefact_id', label: 'Artefact', render: (r) => r.artefact_id },
  { key: 'gate', label: 'Gate', render: (r) => r.gate },
  { key: 'status', label: 'Status', render: (r) => <StatusBadge status={r.status} /> },
  { key: 'opened_at', label: 'Opened', render: (r) => (r.opened_at ? new Date(r.opened_at).toLocaleString() : '—') },
];

/** TS Review page: technical specifications and their TS-gate review cycles. */
export function TsReviewPage() {
  const specsQuery = useQuery({
    queryKey: ['technical-specifications'],
    queryFn: () => technicalSpecificationsApi.list(),
  });

  const reviewsQuery = useQuery({
    queryKey: ['review-cycles', 'TS'],
    queryFn: () => reviewCyclesApi.list({ artefact_type: 'TS' }),
  });

  return (
    <div>
      <PageHeader
        title="TS Review"
        description="Technical specifications generated from functional specifications, and their review cycles."
      />
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={specsQuery.data ?? []}
          columns={specColumns}
          getRowId={(ts) => ts.id}
          isLoading={specsQuery.isLoading}
          error={specsQuery.error}
          emptyMessage="No technical specifications found."
        />
      </Card>
      <Card>
        <DataTable
          items={reviewsQuery.data ?? []}
          columns={reviewColumns}
          getRowId={(r) => r.id}
          isLoading={reviewsQuery.isLoading}
          error={reviewsQuery.error}
          emptyMessage="No TS review cycles found."
        />
      </Card>
    </div>
  );
}
