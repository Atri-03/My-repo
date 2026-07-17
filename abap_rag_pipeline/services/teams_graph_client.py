"""Microsoft Teams Graph API integration — NOT implemented yet.

This module only defines the function signature the transcript_ingest node
will eventually call to pull transcripts directly from Teams instead of a
local file upload. Wire up real MSAL auth + Graph calls here later.
"""
from __future__ import annotations


def fetch_teams_transcript(meeting_id: str) -> str:
    """TODO: Call the Microsoft Graph `/communications/callRecords` or
    `/me/onlineMeetings/{meetingId}/transcripts` API to retrieve the raw
    transcript text for the given meeting.

    Requires: MSAL app registration, GRAPH_TENANT_ID / GRAPH_CLIENT_ID /
    GRAPH_CLIENT_SECRET (see .env.example), and appropriate Graph API
    permissions (OnlineMeetingTranscript.Read.All).
    """
    raise NotImplementedError(
        "Teams Graph API integration is not implemented yet. Upload a "
        "transcript file via the /transcripts/upload endpoint instead."
    )
