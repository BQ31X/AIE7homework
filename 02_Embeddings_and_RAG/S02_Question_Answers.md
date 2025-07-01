#### ❓Question #1:

The default embedding dimension of `text-embedding-3-small` is 1536, as noted above. 

1.1 Is there any way to modify this dimension?


> NOTE: Check out this [API documentation](https://platform.openai.com/docs/api-reference/embeddings/create) for the answer to question #1, and [this documentation](https://platform.openai.com/docs/guides/embeddings/use-cases) for an answer to question #2!

Answer 1.1: yes, according to the documentation, the dimension is an optional integer parameter that you can pass to the embedding:

```python
dimensions
integer
Optional
The number of dimensions the resulting output embeddings should have. Only supported in `text-embedding-3` and later models."
```

Answer 1.2: What technique does OpenAI use to achieve this?
A: Open AI uses vector embedding to turn text chunks into numbers. From the documentation: "An embedding is a vector (list) of floating point numbers. The [distance](https://platform.openai.com/docs/guides/embeddings/use-cases#which-distance-function-should-i-use) between two vectors measures their relatedness."

#### ❓Question #2:

What are the benefits of using an `async` approach to collecting our embeddings?

> NOTE: Determining the core difference between `async` and `sync` will be useful! If you get stuck - ask ChatGPT!

Answer: Async processing allows multiple chunks to be processed in parallel (concurrently), without blocking the program while waiting for each response. This improves speed for processing large batches of text.

#### ❓ Question #3:

When calling the OpenAI API - are there any ways we can achieve more reproducible outputs?

> NOTE: Check out [this section](https://platform.openai.com/docs/guides/text-generation/) of the OpenAI documentation for the answer!

Yes, some options to help achieve more reproducible outputs:
- Pinning your app to a specific model version
- Using consistent message roles and clear instructions
- Creating reusable, well-structured prompts
- Providing relevant context through retrieval-augmented generation (RAG) or RAG in conjunction with other techniques such as Prompt Engineering or Fine-tuning.
#### ❓ Question #4:

What prompting strategies could you use to make the LLM have a more thoughtful, detailed response?

What is that strategy called?

> NOTE: You can look through ["Accessing GPT-3.5-turbo Like a Developer"](https://colab.research.google.com/drive/1mOzbgf4a2SP5qQj33ZxTz2a01-5eXqk2?usp=sharing) for an answer to this question if you get stuck!

To get a more thoughtful, detailed response, use Chain of Thought (CoT) prompting to provide more context. For example, asking the model to "think through your responses step by step" or "explain your reasoning". 
 
You can also use a reasoning model. OpenAI says: "**[Reasoning models](https://platform.openai.com/docs/guides/reasoning)** (such as o3 and o4-mini) "generate an internal chain of thought" so they "excel at understanding complex tasks and multi-step planning."

### ✅ Activity #1 results:

I ran the pipeline with the Michael Eisner prompt:  
**"What is the Michael Eisner Memorial Weak Executive Problem?", k=3**

and these three distance metrics:  
- Cosine similarity  
- Euclidean distance (L2)  
- Taxicab distance (aka Manhattan distance) (L1)

---

**Cosine Similarity**:  

Cosine similarity returned these results:  

**Response:**  
The 'Michael Eisner Memorial Weak Executive Problem' refers to a situation where a CEO or founder, who has expertise in a specific function (such as product management, sales, or marketing), hires a weak executive to manage that same function. This often occurs because the CEO struggles to let go of their original role and influence, leading them to choose someone less competent in order to maintain their own status as the "go-to" person in that area. The term is derived from the experience of Michael Eisner, the former CEO of Disney, who took over ABC and was unable to turn it around despite his previous success, demonstrating how hiring a weak executive can lead to organizational decline. This pattern highlights the tendency of executives to prioritize their own need for control over the capability of their hires (Source 1).  

**Context Count:** 3  
**Similarity Scores:**  
- Source 1: 0.658  
- Source 2: 0.509  
- Source 3: 0.479  

**Based on these 3 chunks:**  

```
[('ordingly.\nSeventh, when hiring the executive to run your former specialty, be\ncareful you don’t hire someone weak on purpose.\nThis sounds silly, but you wouldn’t believe how oaen it happens.\nThe CEO who used to be a product manager who has a weak\nproduct management executive. The CEO who used to be in\nsales who has a weak sales executive. The CEO who used to be\nin marketing who has a weak marketing executive.\nI call this the “Michael Eisner Memorial Weak Executive Problem” — aaer the CEO of Disney who had previously been a brilliant TV network executive. When he bought ABC at Disney, it\npromptly fell to fourth place. His response? “If I had an extra\ntwo days a week, I could turn around ABC myself.” Well, guess\nwhat, he didn’t have an extra two days a week.\nA CEO — or a startup founder — oaen has a hard time letting\ngo of the function that brought him to the party. The result: you\nhire someone weak into the executive role for that function so\nthat you can continue to be “the man” — cons',
```

np.float64(0.6538563767462544)),

```
('m. They have areas where they are truly deXcient in judgment or skill set. That’s just life. Almost nobody is brilliant\nat everything. When hiring and when Hring executives, you\nmust therefore focus on strength rather than lack of weakness. Everybody has severe weaknesses even if you can’t see\nthem yet. When managing, it’s oaen useful to micromanage and\nto provide remedial training around these weaknesses. Doing so\nmay make the diWerence between an executive succeeding or\nfailing.\nFor example, you might have a brilliant engineering executive\nwho generates excellent team loyalty, has terriXc product judgment and makes the trains run on time. This same executive\nmay be very poor at relating to the other functions in the company. She may generate far more than her share of cross-functional conYicts, cut herself oW from critical information, and\nsigniXcantly impede your ability to sell and market eWectively.\nYour alternatives are:\n(a) Macro-manage and give her an annual or quarterly object',
```

np.float64(0.5036012174947992)),

```
('ed?\nIn reality — as opposed to Marc’s warped view of reality — it will\nbe extremely helpful for Marc [if he were actually the CEO,\nwhich he is not] to meet with the new head of engineering daily\nwhen she comes on board and review all of her thinking and\ndecisions. This level of micromanagement will accelerate her\ntraining and improve her long-term eWectiveness. It will make\nher seem smarter to the rest of the organization which will build\ncredibility and conXdence while she comes up to speed. Micromanaging new executives is generally a good idea for a limited\nperiod of time.\nHowever, that is not the only time that it makes sense to micro66 The Pmarca Blog Archives\nmanage executives. It turns out that just about every executive\nin the world has a few things that are seriously wrong with\nthem. They have areas where they are truly deXcient in judgment or skill set. That’s just life. Almost nobody is brilliant\nat everything. When hiring and when Hring executives, you\nmust therefore focus o',

```
np.float64(0.4814102594977529))]


---

**Euclidean Results**:  

Initial results were poor; the search returned irrelevant documents and gave up trying to answer the Eisner question. Once I found the secret sauce (I needed to reverse the sort order), the Euclidean distance returned the same 3 chunks as cosine similarity (above), but with these distance values:  

**Context Count:** 3  
**Similarity Scores:**  
- Source 1: 0.827  
- Source 2: 0.991  
- Source 3: 1.021  


**Euclician Distance Response:**  
The 'Michael Eisner Memorial Weak Executive Problem' refers to a situation where a CEO or startup founder hires a weak executive for a critical function in their company in order to maintain control over that area themselves. This term is named after Michael Eisner, the CEO of Disney, who had previously been successful as a TV network executive. The context notes that after Eisner acquired ABC, the network fell to fourth place, and he attributed this to a lack of time, stating, “If I had an extra two days a week, I could turn around ABC myself.” This reflects the challenge that leaders face in letting go of the functions that contributed to their success, often resulting in the hiring of someone less competent in that role to keep themselves as the central figure or authority in that area (Source 1).  


---

**Taxicab Distance**:  

Here again, once I used the correct approach to reverse the sort order, the taxicab distance returned the same 3 chunks as the other methods. , with below similarity scores and response:  

**Context Count:** 3  
**Similarity Scores:**  
- Source 1: 25.286  
- Source 2: 30.671  
- Source 3: 31.750  

**Taxicab Distance Response:**  
The 'Michael Eisner Memorial Weak Executive Problem' refers to a situation where a CEO or startup founder, who has a strong background in a specific function (such as product management, sales, or marketing), hires a weak executive for that same function. This phenomenon occurs because the leader may have difficulty letting go of their original expertise and chooses to bring in someone less capable in order to maintain control, effectively making themselves "the man" in that area. The context provides an example of Michael Eisner, the former CEO of Disney, who struggled with this issue when he took over ABC, resulting in the network falling to fourth place despite his earlier success as a TV network executive. Eisner's comment about needing "an extra two days a week" to turn things around illustrates this challenge of managing and delegating effectively.  



##### ✅ Enhancement Reflection

While exploring alternative distance measures in the RAG retrieval pipeline, I decided to swap out cosine similarity with Euclidean distance to better understand how distance-based metrics behave in high-dimensional semantic embeddings.

At first, my experiments with Euclidean distance returned irrelevant results and caused the RAG to respond with "I don't know." 😢 This surprised me, since OpenAI documentation states that vectors are normalized to length 1. So, cosine and Euclidean should produce the same rankings. After digging deeper (and sleeping on it), I realized 🚀 the retrieval code in the provided library was sorting the similarity scores in descending order. This is correct for cosine (higher is better) but incorrect for distance-based measures like Euclidean (where lower is better).

First, I modified the .py source code change the sort direction. (I didn't parameterize it, I just changed the hard-coding from reverse=True to reverse=False.) I had to restart the kernel in order to re-import the file with that change. After fixing the sort order, I was able to confirm that Euclidean distance identified the same chunks as cosine similarity, and he RAG pipeline was able to correctly answer the question with consistent context.

That was not a good solution, because it involved modifying the python code. Worse yet, it was a change to a hard-coded value. With some help, I realized that I could invert (negate) the distance values by subtracting them from zero 😆 -- so that the desending sort order would still provide the best results first. Unfotunately, I did not come up with this solution before recording my video 🤦

🎯 From this exercise I learned the importance of:
- understanding the difference in ranking direction between similarity and distance metrics
- not neccesarily settling for the first solution
- paying attention to small implementation details (like sort order), which can dramatically affect program outcomes.



Three things I didn't learn:
1. Which use cases are best suited for RAG versus other approaches.
2. Advanced chunking strategies beyond blog-style text.
3. How RAG systems are benchmarked for accuracy and latency in production.


