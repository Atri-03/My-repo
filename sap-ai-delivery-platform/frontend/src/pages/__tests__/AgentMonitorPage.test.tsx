import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { AgentMonitorPage } from '../AgentMonitorPage';

describe('AgentMonitorPage', () => {
  it('lists active agent runs from the MCP Gateway', async () => {
    renderWithProviders(<AgentMonitorPage />);

    expect(screen.getByRole('heading', { name: 'Agent Monitor' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('wf-1')).toBeInTheDocument();
    });
  });
});
