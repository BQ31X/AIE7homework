#### ❓ Question #1:

What are the three types of query synthesizers doing? Describe each one in simple terms.
Single
MultiHop -abstracct: questions that require reasoning across multiple docs, but remain abstract
MultiHop - specific - questions that are specific to single doc, but need multi doc to answer

#### ❓Question #2:

Why would modifying our chunk size modify the performance of our application?
advantage / disadvantage: 
+ = more context = good
- but, can mean less accuracy - LLM can get lost if too much context

#### ❓Question #3:

Why would modifying our embedding model modify the performance of our application?
because better relationships between embeddings - capture more aspects (dimensions?) of the data, will make retrieval more acccurate
fit larget context, so support bigger chunks.
better embedding= better accuracy
can custom-train/fine-tuned embedding models - more popular than fine-tuning LLMs - give more bang for your buck.
"fine tuning LLM - last resort" $$$!! more resouces needed
get good benefits

google embedding good But $$
cohere makes good inexpensive models; also good at re-ranking model 