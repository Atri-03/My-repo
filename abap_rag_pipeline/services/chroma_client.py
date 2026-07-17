"""ChromaDB client used to retrieve similar past FS/TS documents as few-shot
context for the requirement_extraction node.

For this POC the collection is seeded in-memory/on-disk with a few dummy
FS/TS examples the first time it is accessed, so the pipeline is runnable
without any external data preparation step.
"""
from __future__ import annotations

import hashlib

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

from app.config import settings

_EMBEDDING_DIM = 256


class _OfflineHashingEmbeddingFunction(EmbeddingFunction):
    """Deterministic, dependency-free embedding function for the POC.

    ChromaDB's default embedding function downloads an ONNX model from the
    internet on first use, which is unnecessary friction (and may be blocked)
    for a local POC. This hashing-based bag-of-words embedding keeps the
    demo fully offline while still producing similarity-ranked results.

    TODO: replace with Azure OpenAI text-embedding-3-* (or another hosted
    embedding model) once real historical FS/TS documents are being indexed.
    """

    def __call__(self, input: Documents) -> Embeddings:  # noqa: A002 - Chroma API name
        return [self._embed_text(text) for text in input]

    @staticmethod
    def _embed_text(text: str) -> list[float]:
        vector = [0.0] * _EMBEDDING_DIM
        for token in text.lower().split():
            # MD5 is used purely as a fast, deterministic hash-bucketing
            # function here (not for any cryptographic/security purpose).
            index = int(hashlib.md5(token.encode("utf-8"), usedforsecurity=False).hexdigest(), 16) % _EMBEDDING_DIM
            vector[index] += 1.0
        return vector

_DUMMY_EXAMPLES: list[dict[str, str]] = [
    {
        "id": "example-fs-ts-001",
        "document": (
            "FS/TS Example: Vendor Invoice Approval Workflow\n"
            "Process Flow: 1) AP clerk uploads invoice. 2) System validates vendor "
            "master data. 3) Approver reviews and approves/rejects. 4) Approved "
            "invoices post to FI.\n"
            "Fields: Vendor Number (mandatory), Invoice Amount (mandatory), "
            "Currency, PO Reference (optional), Approval Status.\n"
            "Validations: Vendor must exist in LFA1; invoice amount must be > 0; "
            "duplicate invoice numbers per vendor are rejected.\n"
            "Actors: AP Clerk, Approver, Finance System."
        ),
    },
    {
        "id": "example-fs-ts-002",
        "document": (
            "FS/TS Example: Sales Order Credit Block Release\n"
            "Process Flow: 1) Sales order created and blocked for credit. 2) "
            "Credit manager reviews customer exposure. 3) Manager releases or "
            "rejects the block. 4) Released orders continue to delivery.\n"
            "Fields: Sales Order Number (mandatory), Customer Number (mandatory), "
            "Credit Limit, Exposure Amount, Block Reason.\n"
            "Validations: Customer must have an active credit segment; release "
            "requires manager authorization object F_KKBER.\n"
            "Actors: Sales Rep, Credit Manager, SAP FI-AR."
        ),
    },
    {
        "id": "example-fs-ts-003",
        "document": (
            "FS/TS Example: Material Master Mass Change Request\n"
            "Process Flow: 1) Requestor submits change request with material "
            "list. 2) Data steward validates fields. 3) MDG workflow approves "
            "change. 4) Change transported to production via CATT/LSMW.\n"
            "Fields: Material Number (mandatory), Plant, Base Unit of Measure, "
            "Valuation Class, Change Reason.\n"
            "Validations: Material must exist in MARA; plant must be assigned to "
            "the material; valuation class must be valid for material type.\n"
            "Actors: Requestor, Data Steward, MDG Approver."
        ),
    },
]


def _get_client() -> chromadb.Client:
    return chromadb.PersistentClient(path=settings.chroma_persist_dir)


def get_or_create_seeded_collection() -> chromadb.Collection:
    """Return the FS/TS example collection, seeding dummy documents if empty.

    TODO: replace dummy seed data with a real ingestion job that indexes the
    organization's historical FS/TS document repository.
    """
    client = _get_client()
    collection = client.get_or_create_collection(
        name=settings.chroma_collection_name,
        embedding_function=_OfflineHashingEmbeddingFunction(),
    )

    if collection.count() == 0:
        collection.add(
            ids=[example["id"] for example in _DUMMY_EXAMPLES],
            documents=[example["document"] for example in _DUMMY_EXAMPLES],
        )
    return collection


def retrieve_similar_examples(query_text: str, n_results: int = 2) -> list[str]:
    """Retrieve the most similar past FS/TS documents for few-shot prompting."""
    collection = get_or_create_seeded_collection()
    n_results = max(1, min(n_results, collection.count() or 1))
    results = collection.query(query_texts=[query_text], n_results=n_results)
    documents = results.get("documents") or [[]]
    return documents[0]
