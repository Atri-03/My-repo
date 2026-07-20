import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { WorkflowMonitorPage } from '../WorkflowMonitorPage';

describe('WorkflowMonitorPage', () => {
  it('lists workflow runs and events', async () => {
    renderWithProviders(<WorkflowMonitorPage />);

    expect(screen.getByRole('heading', { name: 'Workflow Monitor' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText('wf-1').length).toBeGreaterThan(0);
    });
    expect(screen.getByText('we-1')).toBeInTheDocument();
  });
});
