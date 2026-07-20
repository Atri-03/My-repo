import { resourceClient } from './client';
import type { BusinessRule, Requirement, RequirementEntity, RequirementRisk, RequirementSet } from './types';

export const requirementSetsApi = resourceClient<RequirementSet>('documentExtraction', '/requirement-sets');
export const requirementsApi = resourceClient<Requirement>('documentExtraction', '/requirements');
export const requirementRisksApi = resourceClient<RequirementRisk>('documentExtraction', '/requirement-risks');
export const requirementEntitiesApi = resourceClient<RequirementEntity>(
  'documentExtraction',
  '/requirement-entities',
);
export const businessRulesApi = resourceClient<BusinessRule>('documentExtraction', '/business-rules');
