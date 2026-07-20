import { Badge } from '@fluentui/react-components';
import type { BadgeProps } from '@fluentui/react-components';

const POSITIVE = new Set(['ACTIVE', 'APPROVED', 'COMPLETED', 'PUBLISHED', 'OK', 'CLOSED']);
const WARNING = new Set(['DRAFT', 'PENDING', 'IN_REVIEW', 'IN_PROGRESS']);
const NEGATIVE = new Set(['REJECTED', 'FAILED', 'ERROR', 'BLOCKED']);

function toneFor(status?: string | null): BadgeProps['color'] {
  if (!status) return 'informative';
  const normalized = status.toUpperCase();
  if (POSITIVE.has(normalized)) return 'success';
  if (WARNING.has(normalized)) return 'warning';
  if (NEGATIVE.has(normalized)) return 'danger';
  return 'informative';
}

/** Colour-coded status badge used across list/detail pages. */
export function StatusBadge({ status }: { status?: string | null }) {
  return (
    <Badge appearance="filled" color={toneFor(status)}>
      {status ?? 'UNKNOWN'}
    </Badge>
  );
}
