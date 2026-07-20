import {
  Table,
  TableBody,
  TableCell,
  TableCellLayout,
  TableHeader,
  TableHeaderCell,
  TableRow,
  Spinner,
  Text,
} from '@fluentui/react-components';
import type { ReactNode } from 'react';

export interface DataTableColumn<T> {
  key: string;
  label: string;
  render: (item: T) => ReactNode;
}

interface DataTableProps<T> {
  items: T[];
  columns: DataTableColumn<T>[];
  getRowId: (item: T) => string;
  isLoading?: boolean;
  error?: unknown;
  emptyMessage?: string;
}

/** Generic, reusable Fluent UI table for rendering lists returned by backend APIs. */
export function DataTable<T>({
  items,
  columns,
  getRowId,
  isLoading,
  error,
  emptyMessage = 'No records found.',
}: DataTableProps<T>) {
  if (isLoading) {
    return <Spinner label="Loading data..." />;
  }

  if (error) {
    return (
      <Text role="alert" style={{ color: 'var(--colorPaletteRedForeground1)' }}>
        Failed to load data: {error instanceof Error ? error.message : 'Unknown error'}
      </Text>
    );
  }

  if (items.length === 0) {
    return <Text>{emptyMessage}</Text>;
  }

  return (
    <Table aria-label="data table" size="small">
      <TableHeader>
        <TableRow>
          {columns.map((column) => (
            <TableHeaderCell key={column.key}>{column.label}</TableHeaderCell>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {items.map((item) => (
          <TableRow key={getRowId(item)}>
            {columns.map((column) => (
              <TableCell key={column.key}>
                <TableCellLayout>{column.render(item)}</TableCellLayout>
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
