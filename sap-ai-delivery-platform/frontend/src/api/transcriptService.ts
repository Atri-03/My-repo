import { resourceClient } from './client';
import type { SourceDocument, Transcript } from './types';

export const sourceDocumentsApi = resourceClient<SourceDocument>('transcript', '/source-documents');
export const transcriptsApi = resourceClient<Transcript>('transcript', '/transcripts');
