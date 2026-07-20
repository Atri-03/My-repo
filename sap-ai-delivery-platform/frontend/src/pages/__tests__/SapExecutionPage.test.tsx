import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { SapExecutionPage } from '../SapExecutionPage';

describe('SapExecutionPage', () => {
  it('lists packages, transports, generated objects, activations, ATC data and execution plans', async () => {
    renderWithProviders(<SapExecutionPage />);

    expect(screen.getByRole('heading', { name: 'SAP Execution' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText('ZRAG_POC').length).toBeGreaterThan(0);
    });
    expect(screen.getAllByText('TRABCD1234').length).toBeGreaterThan(0);
    expect(screen.getAllByText('ZPROGRAM').length).toBeGreaterThan(0);
    expect(screen.getAllByText('ts-1').length).toBeGreaterThan(0);
  });
});
