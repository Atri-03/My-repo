import { resourceClient } from './client';
import type { KnowledgeChunk, KnowledgeSource } from './types';

export const knowledgeSourcesApi = resourceClient<KnowledgeSource>('rag', '/knowledge-sources');
export const knowledgeChunksApi = resourceClient<KnowledgeChunk>('rag', '/knowledge-chunks');
