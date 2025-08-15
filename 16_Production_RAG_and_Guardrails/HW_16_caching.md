

#### 🧪 Embedding Cache Test Results

|Length|Input Summary|First Call (s)|Second Call (s)|Identical|Speedup (x)|
|---|---|---|---|---|---|
|Short|This is a second test sentence|1.2701|0.3354|✅|3.79|
|Short|This is a second test sentence|1.4933|0.5898|✅|2.53|
|Short|This is a second test sentence|0.3612|0.2087|✅|1.73|
|Short (new)|This is a new test sentence|0.2616|1.3536|✅|0.19|
|Short (new)|This is a new test sentence|0.2184|0.7805|✅|0.28|
|Short (new)|This is a new test sentence|0.5805|0.2224|✅|2.61|
|Medium|First sentence of Gettysburg|0.3709|0.2035|✅|1.82|
|Medium|First sentence of Gettysburg|0.2009|0.1987|✅|1.01|
|Long|Full Gettysburg Address|0.2186|0.2718|✅|0.80|
|Long|Full Gettysburg Address|0.2640|0.2759|❌|0.96|
|Long|Full Gettysburg Address|0.2807|0.1951|✅|1.44|
|Short (repeat)|This is a second test sentence|0.2837|0.3639|✅|0.78|
|Short (repeat)|This is a second test sentence|0.3948|0.1544|✅|2.56|

> ✅ = Embeddings were identical  
> ❌ = Embeddings were different (unexpected — may indicate noise, variation, or cache inconsistency)

---
### 📊 Embedding Cache Summary

| Sentence       | Speedup (x) mean | Speedup (x) min | Speedup (x) max | Identical percentage |
| -------------- | ---------------- | --------------- | --------------- | -------------------- |
| Long           | 1.07             | **0.80**        | 1.44            | 67%                  |
| Medium         | 1.42             | 1.01            | 1.82            | 100%                 |
| Short          | 2.68             | 1.73            | 3.79            | 100%                 |
| Short (new)    | 1.03             | 0.19            | 2.61            | 100%                 |
| Short (repeat) | 1.67             | 0.78            | 2.56            | 100%                 |

Short, repeated strings showed the most consistent cache speedup (up to 3.8×), while longer inputs had lower or inconsistent speedups, and one long case even produced a non-identical result.

---


