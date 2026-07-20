import { resourceClient } from './client';
import type { ReviewDecision, SapExecutionPackage } from './types';

export const reviewDecisionsApi = resourceClient<ReviewDecision>('approval', '/review-decisions');
export const sapExecutionPackagesApi = resourceClient<SapExecutionPackage>(
  'approval',
  '/sap-execution-packages',
);
