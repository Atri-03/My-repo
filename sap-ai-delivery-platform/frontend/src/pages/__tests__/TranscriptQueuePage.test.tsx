import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { TranscriptQueuePage } from '../TranscriptQueuePage';

describe('TranscriptQueuePage', () => {
  it('lists transcripts fetched from the transcript service', async () => {
    renderWithProviders(<TranscriptQueuePage />);

    expect(screen.getByRole('heading', { name: 'Transcript Queue' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('t-1')).toBeInTheDocument();
    });
    expect(screen.getByText('sd-1')).toBeInTheDocument();
    expect(screen.getByText('Alice, Bob')).toBeInTheDocument();
  });
});
