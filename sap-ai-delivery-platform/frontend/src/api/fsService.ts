import { resourceClient } from './client';
import type { DocumentTemplate, FunctionalSpecification } from './types';

export const fsDocumentTemplatesApi = resourceClient<DocumentTemplate>('fs', '/document-templates');
export const functionalSpecificationsApi = resourceClient<FunctionalSpecification>(
  'fs',
  '/functional-specifications',
);
