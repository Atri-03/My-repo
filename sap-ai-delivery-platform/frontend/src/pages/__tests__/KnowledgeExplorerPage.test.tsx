import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { KnowledgeExplorerPage } from '../KnowledgeExplorerPage';

describe('KnowledgeExplorerPage', () => {
  it('lists knowledge sources and chunks', async () => {
    renderWithProviders(<KnowledgeExplorerPage />);

    expect(screen.getByRole('heading', { name: 'Knowledge Explorer' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText('ks-1').length).toBeGreaterThan(0);
    });
    expect(screen.getByText('kc-1')).toBeInTheDocument();
  });
});
