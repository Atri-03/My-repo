import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { FsReviewPage } from '../FsReviewPage';

describe('FsReviewPage', () => {
  it('lists functional specifications and FS review cycles', async () => {
    renderWithProviders(<FsReviewPage />);

    expect(screen.getByRole('heading', { name: 'FS Review' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText('fs-1').length).toBeGreaterThan(0);
    });
    expect(screen.getByText('rc-1')).toBeInTheDocument();
  });
});
