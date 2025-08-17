

---

### ⏱️ Agent Latency Comparison (in seconds)

|Query|Simple Agent|Helpfulness Agent|Guarded Agent|
|---|---|---|---|
|1. What is the main purpose of the Direct Loan Program?|3.78|2.58|10.39|
|2. What are the latest developments in AI safety?|12.64|10.04|8.41|
|3. Find recent papers about transformer architectures|5.80|7.42|9.10|
|4. How do the concepts in this document relate to AI trends?|9.94|14.87|9.15|
|5. What is the capital of Mars...?|4.09|5.30|5.60|
|6. What’s the best recipe for chocolate cake?|7.47|5.93|2.24|
|7. My SSN is 123-45-6789...|1.15|1.28|2.88|
|**Average**|**6.41**|**6.77**|**6.97**|

---

### 👀 Conclusion

**The guarded agent was not consistently slower** than the other types — and was actually **faster than the helpfulness agent** on 3 of the 7 queries. It also showed **less variance** between slowest and fastest responses.

#### Why this happened:

- I ran the same queries back-to-back.
    
- Cached completions or embeddings may have helped later agents (especially the guarded one) respond faster.
    
- The **guarded agent’s overhead was ~0.5s–3s**, depending on validation path and input.
    
- The **helpfulness agent** had the highest average latency (6.77s), likely due to more reasoning.
    
- The **simple agent**, while the fastest on average (6.41s), was not always fastest per query.
    

### 🧪 Interpretation

> 🟢 The impact of **caching and execution order** on latency obscures the impact of the complexity of the agent logic, at least in short-burst test loops like this. 


If I randomized query order or cleared cache between runs, the results might differ.
