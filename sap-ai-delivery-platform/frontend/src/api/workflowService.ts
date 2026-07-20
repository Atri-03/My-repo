import { resourceClient } from './client';
import type { WorkflowEvent, WorkflowRun } from './types';

export const workflowRunsApi = resourceClient<WorkflowRun>('workflow', '/workflow-runs');
export const workflowEventsApi = resourceClient<WorkflowEvent>('workflow', '/workflow-events');
