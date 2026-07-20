import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FluentProvider, webLightTheme } from '@fluentui/react-components';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { Layout } from '../Layout';
import { navItems } from '../navItems';

function renderLayoutAt(path: string) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>
      <FluentProvider theme={webLightTheme}>
        <MemoryRouter initialEntries={[path]}>
          <Routes>
            <Route path="/" element={<Layout />}>
              {navItems.map((item) => (
                <Route
                  key={item.path}
                  index={item.path === '/'}
                  path={item.path === '/' ? undefined : item.path.slice(1)}
                  element={<div>{item.label} content</div>}
                />
              ))}
            </Route>
          </Routes>
        </MemoryRouter>
      </FluentProvider>
    </QueryClientProvider>,
  );
}

describe('Layout', () => {
  it('renders navigation links for every page', () => {
    renderLayoutAt('/');
    for (const item of navItems) {
      expect(screen.getByRole('link', { name: item.label })).toBeInTheDocument();
    }
  });

  it('renders the routed page content for the active route', () => {
    renderLayoutAt('/audit-dashboard');
    expect(screen.getByText('Audit Dashboard content')).toBeInTheDocument();
  });
});
