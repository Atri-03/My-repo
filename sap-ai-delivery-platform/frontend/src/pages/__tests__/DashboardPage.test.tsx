import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { DashboardPage } from '../DashboardPage';

describe('DashboardPage', () => {
  it('renders summary counts and service health once data loads', async () => {
    renderWithProviders(<DashboardPage />);

    expect(screen.getByRole('heading', { name: 'Dashboard' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText('1').length).toBeGreaterThan(0);
    });

    expect(screen.getByText('Service Health')).toBeInTheDocument();
  });
});
