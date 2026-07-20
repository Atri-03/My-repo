import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { McpMonitorPage } from '../McpMonitorPage';

describe('McpMonitorPage', () => {
  it('shows MCP Gateway health and registered knowledge sources', async () => {
    renderWithProviders(<McpMonitorPage />);

    expect(screen.getByRole('heading', { name: 'MCP Monitor' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('ok')).toBeInTheDocument();
    });
    expect(screen.getByText('ks-1')).toBeInTheDocument();
  });
});
