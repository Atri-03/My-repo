import { getClient } from './client';
import type {
  GetArtefactResponse,
  GetWorkflowStateResponse,
  ListSourcesResponse,
  SearchDocumentsResponse,
} from './types';

export interface SearchDocumentsRequest {
  query: string;
  source_types?: string[];
  top?: number;
  search_mode?: string;
}

export interface ActiveWorkflowRun {
  id: string;
  current_state: string;
  started_at?: string | null;
  completed_at?: string | null;
  [key: string]: unknown;
}

export const mcpGatewayApi = {
  searchDocuments: async (payload: SearchDocumentsRequest): Promise<SearchDocumentsResponse> => {
    const { data } = await getClient('mcpGateway').post<SearchDocumentsResponse>(
      '/tools/search_documents',
      payload,
    );
    return data;
  },
  listSources: async (): Promise<ListSourcesResponse> => {
    const { data } = await getClient('mcpGateway').get<ListSourcesResponse>('/tools/list_sources');
    return data;
  },
  getLineage: async (knowledgeSourceId: string): Promise<Record<string, unknown>> => {
    const { data } = await getClient('mcpGateway').get(`/tools/get_lineage/${knowledgeSourceId}`);
    return data;
  },
  getFs: async (fsId: string): Promise<GetArtefactResponse> => {
    const { data } = await getClient('mcpGateway').get<GetArtefactResponse>(`/tools/get_fs/${fsId}`);
    return data;
  },
  getTs: async (tsId: string): Promise<GetArtefactResponse> => {
    const { data } = await getClient('mcpGateway').get<GetArtefactResponse>(`/tools/get_ts/${tsId}`);
    return data;
  },
  getWorkflowState: async (workflowRunId: string): Promise<GetWorkflowStateResponse> => {
    const { data } = await getClient('mcpGateway').get<GetWorkflowStateResponse>(
      `/tools/get_workflow_state/${workflowRunId}`,
    );
    return data;
  },
  listActiveRuns: async (): Promise<ActiveWorkflowRun[]> => {
    const { data } = await getClient('mcpGateway').get<ActiveWorkflowRun[]>('/tools/list_active_runs');
    return data;
  },
  submitReviewDecision: async (payload: {
    review_cycle_id: string;
    decided_by: string;
    decision: string;
  }): Promise<Record<string, unknown>> => {
    const { data } = await getClient('mcpGateway').post('/tools/submit_review_decision', payload);
    return data;
  },
};
