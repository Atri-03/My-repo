import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { TsReviewPage } from '../TsReviewPage';

describe('TsReviewPage', () => {
  it('lists technical specifications and TS review cycles', async () => {
    renderWithProviders(<TsReviewPage />);

    expect(screen.getByRole('heading', { name: 'TS Review' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('ts-1')).toBeInTheDocument();
    });
    expect(screen.getByText('rc-1')).toBeInTheDocument();
  });
});
