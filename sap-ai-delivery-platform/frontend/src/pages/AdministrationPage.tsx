import { useQuery } from '@tanstack/react-query';
import { Card } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { StatusBadge } from '../components/StatusBadge';
import { usersApi } from '../api/userService';
import { reviewDecisionsApi, sapExecutionPackagesApi } from '../api/approvalService';
import type { ReviewDecision, SapExecutionPackage, User } from '../api/types';

const userColumns: DataTableColumn<User>[] = [
  { key: 'id', label: 'ID', render: (u) => u.id },
  { key: 'email', label: 'Email', render: (u) => u.email },
  { key: 'display_name', label: 'Name', render: (u) => u.display_name },
  { key: 'role', label: 'Role', render: (u) => u.role ?? '—' },
  {
    key: 'is_active',
    label: 'Active',
    render: (u) => <StatusBadge status={u.is_active ? 'ACTIVE' : 'INACTIVE'} />,
  },
];

const decisionColumns: DataTableColumn<ReviewDecision>[] = [
  { key: 'id', label: 'ID', render: (d) => d.id },
  { key: 'review_cycle_id', label: 'Review Cycle', render: (d) => d.review_cycle_id },
  { key: 'decided_by', label: 'Decided By', render: (d) => d.decided_by },
  { key: 'decision', label: 'Decision', render: (d) => <StatusBadge status={d.decision} /> },
];

const packageColumns: DataTableColumn<SapExecutionPackage>[] = [
  { key: 'id', label: 'ID', render: (p) => p.id },
  {
    key: 'technical_specification_id',
    label: 'Technical Specification',
    render: (p) => p.technical_specification_id,
  },
  { key: 'status', label: 'Status', render: (p) => <StatusBadge status={p.status} /> },
  { key: 'repo_ref', label: 'Repo Ref', render: (p) => p.sap_execution_repo_ref ?? '—' },
];

/** Administration page: user management, review decisions and SAP execution packages. */
export function AdministrationPage() {
  const usersQuery = useQuery({ queryKey: ['users'], queryFn: () => usersApi.list() });
  const decisionsQuery = useQuery({
    queryKey: ['review-decisions'],
    queryFn: () => reviewDecisionsApi.list(),
  });
  const packagesQuery = useQuery({
    queryKey: ['sap-execution-packages'],
    queryFn: () => sapExecutionPackagesApi.list(),
  });

  return (
    <div>
      <PageHeader
        title="Administration"
        description="Platform users, approval decisions and generated SAP execution packages."
      />
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={usersQuery.data ?? []}
          columns={userColumns}
          getRowId={(u) => u.id}
          isLoading={usersQuery.isLoading}
          error={usersQuery.error}
          emptyMessage="No users found."
        />
      </Card>
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={decisionsQuery.data ?? []}
          columns={decisionColumns}
          getRowId={(d) => d.id}
          isLoading={decisionsQuery.isLoading}
          error={decisionsQuery.error}
          emptyMessage="No review decisions recorded."
        />
      </Card>
      <Card>
        <DataTable
          items={packagesQuery.data ?? []}
          columns={packageColumns}
          getRowId={(p) => p.id}
          isLoading={packagesQuery.isLoading}
          error={packagesQuery.error}
          emptyMessage="No SAP execution packages found."
        />
      </Card>
    </div>
  );
}
