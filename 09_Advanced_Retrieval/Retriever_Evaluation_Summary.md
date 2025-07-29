
# Retriever Evaluation Summary (RAGAS)

## Which Retriever Performed Best?

Based on the evaluation metrics for this dataset, the **Ensemble** retriever performed best overall. It achieved the highest **Context Recall** (0.94), maintained low **Noise Sensitivity**, and offered solid performance on **Entity Recall**. Its balanced performance suggests that combining multiple retrieval strategies can help compensate for individual weaknesses. 

The dataset's hybrid structure (descriptive metadata + free-text narrative) benefits from diversity in retrieval style provided by the ensemble of retrieval methods. This diversity helps the retriever recognize relevant content even when useful information is phrased differently or spread across fields.

## Part 1: Main Retriever Comparison

This compares the five main retriever methods: **BM25, Naive, Multi-query, Parent Document, and Ensemble**. Metrics include context recall, entity recall, noise sensitivity, and latency. 

➡️ *Contextual Compression* is excluded from this table because it's not a standalone retrieval method—it's an optimization layered on top of another retriever (Naive).

| Retriever   | Context Recall | Entity Recall | Noise Sensitivity | Latency (s) |
| :---------- | -------------: | ------------: | ----------------: | ----------: |
| bm25        |         0.8667 |         0.454 |            0.2374 |        7.07 |
| naive       |         0.8417 |        0.4445 |            0.2966 |        6.16 |
| multi_query |         0.8667 |        0.4583 |            0.3406 |        6.31 |
| parent_doc  |         0.8083 |        0.3631 |            0.2905 |        5.96 |
| ensemble    |         0.9417 |        0.4396 |            0.2475 |           7 |

## Part 2: Naive vs. Contextual Compression

This focused comparison isolates the impact of applying **Contextual Compression** (via reranking) on top of the **Naive** retriever. By structuring this as a separate table, you're highlighting the direct effect of reranking alone, independent of core retrieval differences.

| Retriever              |   Context Recall |   Entity Recall |   Noise Sensitivity |   Latency (s) |
|:-----------------------|-----------------:|----------------:|--------------------:|--------------:|
| naive                  |           0.8417 |          0.4445 |              0.2966 |          6.16 |
| contextual_compression |           0.7583 |          0.5427 |              0.239  |          8.2  |

## 🔍 Summary

The **Ensemble retriever** achieved the best overall performance on retrieval-specific metrics, with the highest *Context Recall* (0.94) and strong *Noise Sensitivity* performance (0.25), despite relatively high latency (~7s). **BM25** and **Multi-query** also performed well on *Context Recall*, though Multi-query had higher noise sensitivity and slightly worse latency.

When comparing **Naive** to **Contextual Compression** (reranked Naive), we see a tradeoff: compression improved *Entity Recall* from 0.44 to 0.54, but reduced *Context Recall* and increased latency. *Noise Sensitivity* improved slightly. This suggests that reranking can enhance precision around named entities, but may discard useful context and slow down retrieval—potentially impacting time-sensitive systems.

Each approach shows meaningful differences in retrieval quality and efficiency, reinforcing the need to align retriever choice with task requirements (e.g. latency constraints vs. precision needs).

The above latency results were calculated via Python timing code during evaluation. See below for LangSmith cost and latency.

### 💰 LangSmith Cost & Latency: Partial Data

|Retriever|Avg. Latency (s)|Avg. Cost per Query (USD)|
|---|---|---|
|BM25|7.07|$0.01976|
|Contextual Compression|10.10|$0.01683|
|Parent Document|6.79|$0.01775|

LangSmith recorded token usage during the evaluation of **BM25**, **Parent Document**, and **Contextual Compression**.

Because only these three retrievers were fully instrumented, we can’t generalize across all methods — but it’s reasonable to expect that **reranking approaches may cost more**, and **context-heavy retrievers (like Parent Doc)** may also increase token usage during generation.  
**Note:** These cost figures do not include external API usage — for example, **Contextual Compression costs do not reflect Cohere’s reranking charges**, which would increase the true cost per query.

---

### 📝 Footnote: LangSmith Issue

**LangSmith was unavailable** during primary runs due to integration issues and rate limits. Debugging steps included a working session with peer supporter Allan. LangSmith began working but OpenAI quota was exhausted shortly after. After switching to Anthropic, three retrievers (BM25, Parent Document, and Contextual Compression) were instrumented successfully, but further LangSmith logging was halted due to rate limits from Anthropic as well as OpenAI.

