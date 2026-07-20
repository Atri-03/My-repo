import { Subtitle2, Title2, tokens } from '@fluentui/react-components';
import type { ReactNode } from 'react';

interface PageHeaderProps {
  title: string;
  description?: string;
  actions?: ReactNode;
}

/** Consistent page title/description header used at the top of every page. */
export function PageHeader({ title, description, actions }: PageHeaderProps) {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: tokens.spacingVerticalL,
        gap: tokens.spacingHorizontalM,
      }}
    >
      <div>
        <Title2 as="h1">{title}</Title2>
        {description && <Subtitle2 as="p">{description}</Subtitle2>}
      </div>
      {actions}
    </div>
  );
}
