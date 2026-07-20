import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FluentProvider, webLightTheme } from '@fluentui/react-components';
import { DataTable, type DataTableColumn } from '../DataTable';

interface Row {
  id: string;
  name: string;
}

const columns: DataTableColumn<Row>[] = [
  { key: 'id', label: 'ID', render: (r) => r.id },
  { key: 'name', label: 'Name', render: (r) => r.name },
];

function renderTable(props: Partial<Parameters<typeof DataTable<Row>>[0]> = {}) {
  return render(
    <FluentProvider theme={webLightTheme}>
      <DataTable items={[]} columns={columns} getRowId={(r) => r.id} {...props} />
    </FluentProvider>,
  );
}

describe('DataTable', () => {
  it('shows a loading spinner while data is loading', () => {
    renderTable({ isLoading: true });
    expect(screen.getByText('Loading data...')).toBeInTheDocument();
  });

  it('shows an error message when a fetch fails', () => {
    renderTable({ error: new Error('network down') });
    expect(screen.getByText(/Failed to load data: network down/)).toBeInTheDocument();
  });

  it('shows an empty message when there are no items', () => {
    renderTable({ emptyMessage: 'Nothing here.' });
    expect(screen.getByText('Nothing here.')).toBeInTheDocument();
  });

  it('renders a row per item with the configured columns', () => {
    renderTable({ items: [{ id: '1', name: 'First' }, { id: '2', name: 'Second' }] });
    expect(screen.getByText('First')).toBeInTheDocument();
    expect(screen.getByText('Second')).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'Name' })).toBeInTheDocument();
  });
});
