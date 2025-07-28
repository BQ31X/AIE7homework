# Semantic Chunking Threshold Examples

### Sentence Index Visualization

To help visualize chunk boundaries, here are labeled sentence blocks:

```
S1  → S2: 0.04
S2  → S3: 0.05
S3  → S4: 0.06
S4  → S5: 0.50
S5  → S6: 0.15
S6  → S7: 0.35
S7  → S8: 0.12
S8  → S9: 0.13
S9  → S10: 0.40
S10 → S11: 0.70
```

Using the sample list of adjacent semantic distances:

```python
distances = [0.04, 0.05, 0.06, 0.50, 0.15, 0.35, 0.12, 0.13, 0.40, 0.70]
```

To aid in visualizing the threshold calculations, we sort the list:

```python
sorted_distances = [0.04, 0.05, 0.06, 0.12, 0.13, 0.15, 0.35, 0.40, 0.50, 0.70]
```

> Note: Chunking logic always operates on the **original sentence order**, but sorting helps analyze percentile, IQR, and other thresholds more easily.

## 1. Percentile Method

- **80th Percentile**: 0.420
- Would split at values above **0.420**

**Chunks (80th percentile):**

- Chunk 1: Sentences 1–4
- Chunk 2: Sentences 5–10
- Chunk 3: Sentence 11

## 2. Interquartile Method (IQR)

- **Q1**: 0.075
- **Q3**: 0.388
- **IQR**: 0.312
- **Threshold**: Q3 + 1.5 × IQR = 0.856
- Would split at values above **0.856**

**Chunks (IQR):**

- Chunk 1: Sentences 1–11

## 3. Standard Deviation Method

- **Mean**: 0.250
- **StdDev**: 0.214
- **Threshold**: Mean + 1.5 × StdDev = 0.571
- Would split at values above **0.571**

**Chunks (StdDev):**

- Chunk 1: Sentences 1–10
- Chunk 2: Sentence 11

## 4. Gradient Method

- **Gradients**: [0.01, 0.01, 0.44, -0.35, 0.20, -0.23, 0.01, 0.27, 0.30]

**Gradient Calculation Table:**

| Step | Calculation | Result |
| ---- | ----------- | ------ |
| 0    | 0.05 − 0.04 | 0.01   |
| 1    | 0.06 − 0.05 | 0.01   |
| 2    | 0.50 − 0.06 | 0.44   |
| 3    | 0.15 − 0.50 | -0.35  |
| 4    | 0.35 − 0.15 | 0.20   |
| 5    | 0.12 − 0.35 | -0.23  |
| 6    | 0.13 − 0.12 | 0.01   |
| 7    | 0.40 − 0.13 | 0.27   |
| 8    | 0.70 − 0.40 | 0.30   |

- **Threshold**: 0.10
- Would split at indices where gradient > 0.10, e.g., indices 2, 4, 7, 8

**Chunks (Gradient):**

- Chunk 1: Sentences 1–3
- Chunk 2: Sentence 4
- Chunk 3: Sentences 5–7
- Chunk 4: Sentence 8
- Chunk 5: Sentences 9–11

### Summary of Method Behavior

This example highlights how each chunking method reacts to different types of semantic transitions:

- **Percentile**: Sensitive to the top X% of distances. In this case, it split at 0.50 and 0.70, both large values within the top 20%, showing it's effective at catching high outliers but will ignore smaller jumps.

- **Interquartile (IQR)**: Designed to detect only extreme outliers. Since no values exceeded Q3 + 1.5×IQR, it created just one large chunk. This method is the most conservative and best suited for very clean data with rare sharp topic shifts.

- **Standard Deviation**: Responds to values significantly higher than the mean. It only split on the final distance (0.70), which was the most extreme jump relative to the dataset's average. This approach strikes a balance between flexibility and stability.

- **Gradient**: Highly sensitive to sudden local changes, even when absolute values aren't extreme. It produced the most granular result, splitting at sharp increases like 0.44 and 0.27, as well as subtler jumps. This method is ideal for detecting abrupt transitions in otherwise smooth flows.
