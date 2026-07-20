import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { ConfigurationPage } from '../ConfigurationPage';

describe('ConfigurationPage', () => {
  it('lists tenants, projects and document templates', async () => {
    renderWithProviders(<ConfigurationPage />);

    expect(screen.getByRole('heading', { name: 'Configuration' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Acme Corp')).toBeInTheDocument();
    });
    expect(screen.getByText('S/4HANA Rollout')).toBeInTheDocument();
    expect(screen.getByText('Default FS Template')).toBeInTheDocument();
  });
});
