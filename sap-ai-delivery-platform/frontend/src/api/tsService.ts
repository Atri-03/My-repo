import { resourceClient } from './client';
import type { TechnicalSpecification } from './types';

export const technicalSpecificationsApi = resourceClient<TechnicalSpecification>(
  'ts',
  '/technical-specifications',
);
