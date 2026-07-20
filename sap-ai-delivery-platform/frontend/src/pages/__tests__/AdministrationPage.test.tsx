import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/test-utils';
import { AdministrationPage } from '../AdministrationPage';

describe('AdministrationPage', () => {
  it('lists users, review decisions and SAP execution packages', async () => {
    renderWithProviders(<AdministrationPage />);

    expect(screen.getByRole('heading', { name: 'Administration' })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('user@example.com')).toBeInTheDocument();
    });
    expect(screen.getByText('rd-1')).toBeInTheDocument();
    expect(screen.getByText('pkg-1')).toBeInTheDocument();
  });
});
