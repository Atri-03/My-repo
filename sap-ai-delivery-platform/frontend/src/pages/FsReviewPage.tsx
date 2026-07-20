import { useQuery } from '@tanstack/react-query';
import { Card } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { StatusBadge } from '../components/StatusBadge';
import { functionalSpecificationsApi } from '../api/fsService';
import { reviewCyclesApi } from '../api/reviewService';
import type { FunctionalSpecification, ReviewCycle } from '../api/types';

const specColumns: DataTableColumn<FunctionalSpecification>[] = [
  { key: 'id', label: 'ID', render: (fs) => fs.id },
  { key: 'requirement_set_id', label: 'Requirement Set', render: (fs) => fs.requirement_set_id },
  { key: 'version', label: 'Version', render: (fs) => String(fs.version ?? '—') },
  { key: 'status', label: 'Status', render: (fs) => <StatusBadge status={fs.status} /> },
  {
    key: 'regeneration_count',
    label: 'Regenerations',
    render: (fs) => String(fs.regeneration_count ?? 0),
  },
];

const reviewColumns: DataTableColumn<ReviewCycle>[] = [
  { key: 'id', label: 'ID', render: (r) => r.id },
  { key: 'artefact_id', label: 'Artefact', render: (r) => r.artefact_id },
  { key: 'gate', label: 'Gate', render: (r) => r.gate },
  { key: 'status', label: 'Status', render: (r) => <StatusBadge status={r.status} /> },
  { key: 'opened_at', label: 'Opened', render: (r) => (r.opened_at ? new Date(r.opened_at).toLocaleString() : '—') },
];

/** FS Review page: functional specifications and their FS-gate review cycles. */
export function FsReviewPage() {
  const specsQuery = useQuery({
    queryKey: ['functional-specifications'],
    queryFn: () => functionalSpecificationsApi.list(),
  });

  const reviewsQuery = useQuery({
    queryKey: ['review-cycles', 'FS'],
    queryFn: () => reviewCyclesApi.list({ artefact_type: 'FS' }),
  });

  return (
    <div>
      <PageHeader
        title="FS Review"
        description="Functional specifications generated from requirements, and their review cycles."
      />
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={specsQuery.data ?? []}
          columns={specColumns}
          getRowId={(fs) => fs.id}
          isLoading={specsQuery.isLoading}
          error={specsQuery.error}
          emptyMessage="No functional specifications found."
        />
      </Card>
      <Card>
        <DataTable
          items={reviewsQuery.data ?? []}
          columns={reviewColumns}
          getRowId={(r) => r.id}
          isLoading={reviewsQuery.isLoading}
          error={reviewsQuery.error}
          emptyMessage="No FS review cycles found."
        />
      </Card>
    </div>
  );
}
