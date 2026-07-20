import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { AuditDashboardPage } from '../AuditDashboardPage';

describe('AuditDashboardPage', () => {
  it('lists audit log entries', async () => {
    renderWithProviders(<AuditDashboardPage />);

    expect(screen.getByRole('heading', { name: 'Audit Dashboard' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('audit-1')).toBeInTheDocument();
    });
    expect(screen.getByText('CREATE')).toBeInTheDocument();
  });
});
