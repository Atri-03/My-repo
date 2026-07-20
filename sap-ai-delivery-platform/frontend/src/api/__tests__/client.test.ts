import { describe, expect, it } from 'vitest';
import { transcriptsApi } from '../transcriptService';
import { auditLogEntriesApi } from '../auditService';

describe('resourceClient', () => {
  it('lists transcripts from the mocked Transcript Service', async () => {
    const transcripts = await transcriptsApi.list();
    expect(transcripts).toHaveLength(1);
    expect(transcripts[0]).toMatchObject({ id: 't-1', parsed_format: 'TEXT' });
  });

  it('lists audit log entries from the mocked Audit Service', async () => {
    const entries = await auditLogEntriesApi.list();
    expect(entries).toHaveLength(1);
    expect(entries[0]).toMatchObject({ id: 'audit-1', action: 'CREATE' });
  });
});
