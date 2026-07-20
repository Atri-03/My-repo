import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FluentProvider, webLightTheme } from '@fluentui/react-components';
import { StatusBadge } from '../StatusBadge';

function renderBadge(status?: string | null) {
  return render(
    <FluentProvider theme={webLightTheme}>
      <StatusBadge status={status} />
    </FluentProvider>,
  );
}

describe('StatusBadge', () => {
  it('renders the given status text', () => {
    renderBadge('APPROVED');
    expect(screen.getByText('APPROVED')).toBeInTheDocument();
  });

  it('falls back to UNKNOWN when status is missing', () => {
    renderBadge(null);
    expect(screen.getByText('UNKNOWN')).toBeInTheDocument();
  });
});
