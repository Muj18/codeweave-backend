### RAG Pipeline Troubleshooting

**Key Symptoms**
- Query returns irrelevant or hallucinated answers
- Empty or incomplete responses despite documents existing
- Latency spikes during retrieval or generation
- Vector store lookups return 0 results when context should match

**Immediate Triage**
- Check embeddings creation process: ensure consistent model (e.g., `text-embedding-ada-002`)
- Verify documents are chunked and indexed properly in the vector DB
- Inspect logs for retrieval queries and similarity scores
- Confirm vector DB (Pinecone, Weaviate, FAISS, Qdrant) is reachable and healthy
- Validate prompt template includes retrieved context when sent to LLM

**Safe Fix**
~~~python
# Example: RAG pipeline with context injection
def rag_query(llm, vector_db, query):
    # Retrieve top 5 most relevant docs
    docs = vector_db.similarity_search(query, k=5)

    context = "\n\n".join([d.page_content for d in docs])
    prompt = f"""
    Use the following context to answer the question.
    Context:
    {context}

    Question: {query}
    """
    return llm(prompt)
~~~

**Cloud & Platform Notes**
- Monitor vector DB query latency (P95/P99)
- Ensure embedding model is not rate-limited or inconsistent
- Validate storage size — large corpora may require sharding/index optimization
- If deployed in Kubernetes, confirm vector DB pods have adequate CPU/memory for ANN search

**Monitoring & Prevention**
- Add metrics for retrieval hit rate and embedding generation failures
- Alert on queries returning no results
- Periodically re-embed data when models are updated
- Cache frequent queries to reduce LLM and DB load