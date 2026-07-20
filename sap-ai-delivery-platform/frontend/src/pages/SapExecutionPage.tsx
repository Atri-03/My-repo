import { useQuery } from '@tanstack/react-query';
import { Card, Title3 } from '@fluentui/react-components';
import { PageHeader } from '../components/PageHeader';
import { DataTable, type DataTableColumn } from '../components/DataTable';
import { StatusBadge } from '../components/StatusBadge';
import {
  activationsApi,
  atcRemediationsApi,
  atcRunsApi,
  executionPlansApi,
  generatedObjectsApi,
  sapPackagesApi,
  sapTransportsApi,
} from '../api/sapExecutionService';
import type {
  Activation,
  AtcRemediation,
  AtcRun,
  ExecutionPlan,
  GeneratedObject,
  SapPackage,
  SapTransport,
} from '../api/types';

const packageColumns: DataTableColumn<SapPackage>[] = [
  { key: 'package_name', label: 'Package', render: (p) => p.package_name },
  { key: 'description', label: 'Description', render: (p) => p.description },
  { key: 'software_component', label: 'Software Component', render: (p) => p.software_component },
  { key: 'status', label: 'Status', render: (p) => <StatusBadge status={p.status} /> },
];

const transportColumns: DataTableColumn<SapTransport>[] = [
  { key: 'transport_request', label: 'Transport', render: (t) => t.transport_request },
  { key: 'description', label: 'Description', render: (t) => t.description },
  { key: 'transport_type', label: 'Type', render: (t) => t.transport_type },
  { key: 'status', label: 'Status', render: (t) => <StatusBadge status={t.status} /> },
];

const objectColumns: DataTableColumn<GeneratedObject>[] = [
  { key: 'object_name', label: 'Object', render: (o) => o.object_name },
  { key: 'object_type', label: 'Type', render: (o) => o.object_type },
  { key: 'package', label: 'Package', render: (o) => o.package },
  { key: 'transport_request', label: 'Transport', render: (o) => o.transport_request },
  { key: 'status', label: 'Status', render: (o) => <StatusBadge status={o.status} /> },
];

const activationColumns: DataTableColumn<Activation>[] = [
  { key: 'object_name', label: 'Object', render: (a) => a.object_name },
  { key: 'object_type', label: 'Type', render: (a) => a.object_type },
  { key: 'status', label: 'Status', render: (a) => <StatusBadge status={a.status} /> },
  {
    key: 'activated_at',
    label: 'Activated',
    render: (a) => (a.activated_at ? new Date(a.activated_at).toLocaleString() : '—'),
  },
];

const atcRunColumns: DataTableColumn<AtcRun>[] = [
  { key: 'object_name', label: 'Object', render: (a) => a.object_name },
  { key: 'variant', label: 'Variant', render: (a) => a.variant },
  { key: 'status', label: 'Status', render: (a) => <StatusBadge status={a.status} /> },
  { key: 'findings', label: 'Findings', render: (a) => String(a.findings?.length ?? 0) },
];

const atcRemediationColumns: DataTableColumn<AtcRemediation>[] = [
  { key: 'object_name', label: 'Object', render: (a) => a.object_name },
  { key: 'finding_ids', label: 'Findings', render: (a) => a.finding_ids.join(', ') },
  { key: 'auto_apply', label: 'Auto-applied', render: (a) => (a.auto_apply ? 'Yes' : 'No') },
  { key: 'status', label: 'Status', render: (a) => <StatusBadge status={a.status} /> },
];

const planColumns: DataTableColumn<ExecutionPlan>[] = [
  { key: 'technical_specification_id', label: 'Technical Specification', render: (p) => p.technical_specification_id },
  { key: 'package_name', label: 'Package', render: (p) => p.package_name ?? '—' },
  { key: 'steps', label: 'Steps', render: (p) => String(p.steps?.length ?? 0) },
  { key: 'status', label: 'Status', render: (p) => <StatusBadge status={p.status} /> },
];

/**
 * SAP Execution page: the in-repository SAP Execution bounded context —
 * packages, transports, generated objects (ABAP/RAP/CDS/OData),
 * activations, ATC runs/remediations, and SAP Solution Architect Agent
 * execution plans. Backed by `sap_execution_service`.
 */
export function SapExecutionPage() {
  const packagesQuery = useQuery({ queryKey: ['sap-packages'], queryFn: () => sapPackagesApi.list() });
  const transportsQuery = useQuery({ queryKey: ['sap-transports'], queryFn: () => sapTransportsApi.list() });
  const objectsQuery = useQuery({ queryKey: ['generated-objects'], queryFn: () => generatedObjectsApi.list() });
  const activationsQuery = useQuery({ queryKey: ['activations'], queryFn: () => activationsApi.list() });
  const atcRunsQuery = useQuery({ queryKey: ['atc-runs'], queryFn: () => atcRunsApi.list() });
  const atcRemediationsQuery = useQuery({
    queryKey: ['atc-remediations'],
    queryFn: () => atcRemediationsApi.list(),
  });
  const plansQuery = useQuery({ queryKey: ['execution-plans'], queryFn: () => executionPlansApi.list() });

  return (
    <div>
      <PageHeader
        title="SAP Execution"
        description="Packages, transports, generated objects, activations, ATC quality gates and SAP Solution Architect Agent execution plans, subject to the Human-in-the-Loop governance gates 3-5."
      />

      <Title3>Packages &amp; Transports</Title3>
      <Card style={{ margin: '8px 0 16px' }}>
        <DataTable
          items={packagesQuery.data ?? []}
          columns={packageColumns}
          getRowId={(p) => p.id}
          isLoading={packagesQuery.isLoading}
          error={packagesQuery.error}
          emptyMessage="No SAP packages created yet."
        />
      </Card>
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={transportsQuery.data ?? []}
          columns={transportColumns}
          getRowId={(t) => t.id}
          isLoading={transportsQuery.isLoading}
          error={transportsQuery.error}
          emptyMessage="No transport requests created yet."
        />
      </Card>

      <Title3>Generated Objects &amp; Activation</Title3>
      <Card style={{ margin: '8px 0 16px' }}>
        <DataTable
          items={objectsQuery.data ?? []}
          columns={objectColumns}
          getRowId={(o) => o.id}
          isLoading={objectsQuery.isLoading}
          error={objectsQuery.error}
          emptyMessage="No ABAP/RAP/CDS/OData objects generated yet."
        />
      </Card>
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={activationsQuery.data ?? []}
          columns={activationColumns}
          getRowId={(a) => a.id}
          isLoading={activationsQuery.isLoading}
          error={activationsQuery.error}
          emptyMessage="No activations recorded yet."
        />
      </Card>

      <Title3>ATC Orchestration &amp; Remediation</Title3>
      <Card style={{ margin: '8px 0 16px' }}>
        <DataTable
          items={atcRunsQuery.data ?? []}
          columns={atcRunColumns}
          getRowId={(a) => a.id}
          isLoading={atcRunsQuery.isLoading}
          error={atcRunsQuery.error}
          emptyMessage="No ATC runs recorded yet."
        />
      </Card>
      <Card style={{ marginBottom: '16px' }}>
        <DataTable
          items={atcRemediationsQuery.data ?? []}
          columns={atcRemediationColumns}
          getRowId={(a) => a.id}
          isLoading={atcRemediationsQuery.isLoading}
          error={atcRemediationsQuery.error}
          emptyMessage="No ATC remediations recorded yet."
        />
      </Card>

      <Title3>SAP Solution Architect Agent — Execution Plans</Title3>
      <Card style={{ margin: '8px 0' }}>
        <DataTable
          items={plansQuery.data ?? []}
          columns={planColumns}
          getRowId={(p) => p.id}
          isLoading={plansQuery.isLoading}
          error={plansQuery.error}
          emptyMessage="No execution plans proposed yet."
        />
      </Card>
    </div>
  );
}
