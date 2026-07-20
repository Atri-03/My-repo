import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, TabList, Tab, type SelectTabEventHandler } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { StatusBadge } from '../components/StatusBadge';
import { requirementSetsApi, requirementsApi } from '../api/documentExtractionService';
import type { Requirement, RequirementSet } from '../api/types';

const setColumns: DataTableColumn<RequirementSet>[] = [
  { key: 'id', label: 'ID', render: (s) => s.id },
  { key: 'transcript_id', label: 'Transcript', render: (s) => s.transcript_id },
  { key: 'version', label: 'Version', render: (s) => String(s.version ?? '—') },
  { key: 'status', label: 'Status', render: (s) => <StatusBadge status={s.status} /> },
];

const requirementColumns: DataTableColumn<Requirement>[] = [
  { key: 'id', label: 'ID', render: (r) => r.id },
  { key: 'type', label: 'Type', render: (r) => r.type },
  { key: 'title', label: 'Title', render: (r) => r.title },
  { key: 'priority', label: 'Priority', render: (r) => r.priority ?? '—' },
  { key: 'description', label: 'Description', render: (r) => r.description },
];

/** Requirement View page: browse extracted requirement sets and their requirements. */
export function RequirementViewPage() {
  const [selectedSetId, setSelectedSetId] = useState<string | undefined>(undefined);

  const requirementSetsQuery = useQuery({
    queryKey: ['requirement-sets'],
    queryFn: () => requirementSetsApi.list(),
  });

  const activeSetId = selectedSetId ?? requirementSetsQuery.data?.[0]?.id;

  const requirementsQuery = useQuery({
    queryKey: ['requirements', activeSetId],
    queryFn: () => requirementsApi.list({ requirement_set_id: activeSetId }),
    enabled: Boolean(activeSetId),
  });

  const onTabSelect: SelectTabEventHandler = (_e, data) => setSelectedSetId(String(data.value));

  return (
    <div>
      <PageHeader
        title="Requirement View"
        description="Requirement sets extracted from transcripts and their individual requirements."
      />
      <Card style={{ marginBottom: '16px', padding: '12px' }}>
        <DataTable
          items={requirementSetsQuery.data ?? []}
          columns={setColumns}
          getRowId={(s) => s.id}
          isLoading={requirementSetsQuery.isLoading}
          error={requirementSetsQuery.error}
          emptyMessage="No requirement sets found."
        />
      </Card>
      {requirementSetsQuery.data && requirementSetsQuery.data.length > 0 && (
        <>
          <TabList selectedValue={activeSetId} onTabSelect={onTabSelect} style={{ marginBottom: '12px' }}>
            {requirementSetsQuery.data.map((set) => (
              <Tab key={set.id} value={set.id}>
                {set.id.slice(0, 8)}
              </Tab>
            ))}
          </TabList>
          <Card>
            <DataTable
              items={requirementsQuery.data ?? []}
              columns={requirementColumns}
              getRowId={(r) => r.id}
              isLoading={requirementsQuery.isLoading}
              error={requirementsQuery.error}
              emptyMessage="No requirements found for this set."
            />
          </Card>
        </>
      )}
    </div>
  );
}
