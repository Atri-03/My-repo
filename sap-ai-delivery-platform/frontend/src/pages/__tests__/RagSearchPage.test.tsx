import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithProviders } from '../../test/test-utils';
import { RagSearchPage } from '../RagSearchPage';

describe('RagSearchPage', () => {
  it('runs a search and displays results returned by the MCP Gateway', async () => {
    renderWithProviders(<RagSearchPage />);

    expect(screen.getByRole('heading', { name: 'RAG Search' })).toBeInTheDocument();
    expect(screen.getByText('Run a search to see results.')).toBeInTheDocument();

    const user = userEvent.setup();
    await user.type(screen.getByPlaceholderText(/sales order pricing procedure/i), 'pricing procedure');
    await user.click(screen.getByRole('button', { name: 'Search' }));

    await waitFor(() => {
      expect(screen.getByText('Sample indexed chunk text')).toBeInTheDocument();
    });
  });
});
