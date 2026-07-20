import { useQuery } from '@tanstack/react-query';
import { Card } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { StatusBadge } from '../components/StatusBadge';
import { projectsApi, tenantsApi } from '../api/userService';
import { fsDocumentTemplatesApi } from '../api/fsService';
import type { DocumentTemplate, Project, Tenant } from '../api/types';

const tenantColumns: DataTableColumn<Tenant>[] = [
  { key: 'id', label: 'ID', render: (t) => t.id },
  { key: 'name', label: 'Name', render: (t) => t.name },
  { key: 'tier', label: 'Tier', render: (t) => t.tier ?? '—' },
  { key: 'status', label: 'Status', render: (t) => <StatusBadge status={t.status} /> },
];

const projectColumns: DataTableColumn<Project>[] = [
  { key: 'id', label: 'ID', render: (p) => p.id },
  { key: 'tenant_id', label: 'Tenant', render: (p) => p.tenant_id },
  { key: 'name', label: 'Name', render: (p) => p.name },
  { key: 'repo', label: 'SAP Execution Repo', render: (p) => p.sap_execution_repo_url ?? '—' },
];

const templateColumns: DataTableColumn<DocumentTemplate>[] = [
  { key: 'id', label: 'ID', render: (t) => t.id },
  { key: 'name', label: 'Name', render: (t) => t.name },
  { key: 'type', label: 'Type', render: (t) => t.type ?? '—' },
  { key: 'version', label: 'Version', render: (t) => String(t.version ?? '—') },
  {
    key: 'is_active',
    label: 'Active',
    render: (t) => <StatusBadge status={t.is_active ? 'ACTIVE' : 'INACTIVE'} />,
  },
];

/** Configuration page: tenants, projects and document templates that drive platform behaviour. */
export function ConfigurationPage() {
  const tenantsQuery = useQuery({ queryKey: ['tenants'], queryFn: () => tenantsApi.list() });
  const projectsQuery = useQuery({ queryKey: ['projects'], queryFn: () => projectsApi.list() });
  const templatesQuery = useQuery({
    queryKey: ['document-templates'],
    queryFn: () => fsDocumentTemplatesApi.list(),
  });

  return (
    <div>
      <PageHeader
        title="Configuration"
        description="Tenants, projects and document templates used to configure the platform."
      />
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={tenantsQuery.data ?? []}
          columns={tenantColumns}
          getRowId={(t) => t.id}
          isLoading={tenantsQuery.isLoading}
          error={tenantsQuery.error}
          emptyMessage="No tenants configured."
        />
      </Card>
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={projectsQuery.data ?? []}
          columns={projectColumns}
          getRowId={(p) => p.id}
          isLoading={projectsQuery.isLoading}
          error={projectsQuery.error}
          emptyMessage="No projects configured."
        />
      </Card>
      <Card>
        <DataTable
          items={templatesQuery.data ?? []}
          columns={templateColumns}
          getRowId={(t) => t.id}
          isLoading={templatesQuery.isLoading}
          error={templatesQuery.error}
          emptyMessage="No document templates configured."
        />
      </Card>
    </div>
  );
}
