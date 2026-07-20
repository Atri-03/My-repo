import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { RequirementViewPage } from '../RequirementViewPage';

describe('RequirementViewPage', () => {
  it('lists requirement sets and drills into requirements', async () => {
    renderWithProviders(<RequirementViewPage />);

    expect(screen.getByRole('heading', { name: 'Requirement View' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText('rs-1').length).toBeGreaterThan(0);
    });

    await waitFor(() => {
      expect(screen.getByText('Sample requirement')).toBeInTheDocument();
    });
  });
});
