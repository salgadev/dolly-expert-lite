---
title: dolly-expert-builder
app_file: app.py
sdk: gradio
sdk_version: 3.34.0
---
# dolly-expert-lite
A lightweight Dolly-v2 powered assistant that can answer domain-specific questions and keep a conversation. It's expert systems in the era of LLMs.

Submission to the "So you think you can hack": open-source LLMs (e.g., OpenAssistant, MPT, Dolly, etc.) DevPost Hackathon.

- [Dolly Expert Builder @ HuggingFace Spaces](https://huggingface.co/spaces/salgadev/dolly-expert-builder)
- [Published Databricks Notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/3137554102764464/588418364077599/6633303612634971/latest.html)
- [Jupyter Notebook - GitHub Version](https://github.com/socd06/dolly-expert-lite/blob/main/Dolly_3B_Building_Code_Expert_Question_Answering_with_Memory.ipynb)


## Inspiration
### Expert systems
 [Expert Systems](https://en.wikipedia.org/wiki/Expert_system) used to be big in artificial intelligence. They mimic the decision-making capabilities of a human expert in a particular field and can provide substantial value in many use cases. The main drawback of old school expert systems was that they had to be programmed using Boolean statements or a similar logic, taking considerable time and resources. In many occasions, this approach defeated the purpose of having a readily available expert for the task at hand.

### Closed-source LLMs
Closed-source LLM applications like ChatGPT3.5 and ChatGPT-4 are gigantic models that are very good a large number of tasks. They do have limitations such as hallucinations when they don't know how to respond or when the answer is online and they don't have access to the internet or files. Some times, these hallucinations will be told in very convincing ways and whenever one tries to implement them they will turn out to be flat-out false or incorrect. These models have enormous context windows so people can help them do
whatever task they struggle with by providing lots of information and implementing prompt engineering techniques. This makes more than one think that only the big companies with closed source code can develop and deploy LLM applications.

## What it does
Dolly Expert Lite leverages [dolly-v2-3b](dolly-v2-3b), the lightweight version of [dolly-v2-12b](https://huggingface.co/databricks/dolly-v2-12b), an open-source large language model ([LLM](https://en.wikipedia.org/wiki/Large_language_model)) to answer domain-specific questions using retrieval in custom-made vector databases. In this example deployment, [dolly-expert-builder](https://huggingface.co/spaces/salgadev/dolly-expert-builder) retrieves information from the [Ontario (Canada) building code](https://www.buildingcode.online/) to answer specific questions about construction, plumbing, electrical wiring and ventilation as per the official government code. [dolly-expert-builder](https://huggingface.co/spaces/salgadev/dolly-expert-builder) can provide coherent and factually correct information with sources and can serve as guidance suitable for tradespeople (plumbers, electricians, mechanics, home builders) as well as engineers and architects to aid in regulatory compliance while performing work. 

By following this method, individuals and organizations can use their local data to make expert assistants able to answer domain-specific questions. Possible use cases include:
- Spelling out Regulatory/Legal requirements
- On-boarding and Training Support
- Explaining Quality Systems 
- Literature Reviews
- Documentation search 


## How we built it
- Model: [dolly-v2-3b](dolly-v2-3b) to exemplify lightweight development and deployment
- Framework: [LangChain](https://github.com/hwchase17/langchain) to make  the question answering chain and because of its integration with ChromaDB
- Text Embeddings: [Text Embeddings by Weakly-Supervised Contrastive Pre-training (E5-base-v2)](https://huggingface.co/intfloat/e5-base-v2). Because of their high score in retrieval tasks as per the [MTEB English Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [The Ontario (Canada) Building Code](https://www.buildingcode.online/): To make an example of how non-tech workers can benefit from LLM applications. The code page is not easy to navigate because the sections are just named "Section 1", "Section 2"..., "Section 14". Used their website to parse and convert into the vector store.
- Vector Store: [ChromaDB](https://github.com/chroma-core/chroma)
- Deployment: [HuggingFace Spaces](https://huggingface.co/) and [gradio](https://gradio.app/). Deployment available here: [Dolly Expert Builder](https://huggingface.co/spaces/salgadev/dolly-expert-builder)


## Challenges we ran into
Since the tools are so new, some divergences from the standard use cases cause errors. For example:
- Failure to use memory and sources in the same question answering chain in LangChain. A workaround was implemented by creating a class that inherited from the memory class.
- Error when web scrapping using sitemaps while on a Jupyter Notebook.  This could be circumvented applying the nest_asyncio workaround.
- Vector database not loading. Another early development LangChain issue, it saved partially when using ```persists_directory``` in the ChromaDB initialization and it would not load later in a separate instance because the .persists() method was not called. This had to be redone and committed again for the database to be finally available.
- Gradio app not launching on Jupyter Notebook. The previous workaround changed the local installation of asyncio, which is a Gradio requirement, making it unusable during the same runtime. To avoid this, the vector database was made in a separate notebook and committed to the repo.
- Very slow inference on CPU. Since there are no official quantized Dolly models available, using CPU for inference had very high latency. I also ran out of my databricks free trial by the time of submission. Fortunately, the code was functional by then and I was able to deploy and test online on a t4-small space.  


## Accomplishments that we're proud of
Being able to make a functional lightweight prototype of an LLM application using an open-source model like Dolly and deploying it as a HuggingFace Space. Being able to show that LLM applications are for everyone and that the open-source ecosystem is just as capable as the closed-source pioneers.


## What we learned
In terms of general software development knowledge, I learned to troubleshoot packages conflicting with each other, learned that Python has to be restarted depending on what dependencies are installed or that sometimes it's better to compartmentalize tasks instead of trying to do everything at once. I also learned the basics of Gradio to be able to make the app. And most importantly, I learned to better navigate [GitHub issues](https://github.com/issues) and [StackOverflow](https://stackoverflow.co/) posts to find workarounds for the problems I encountered.

In terms of LLM-related knowledge, I learned about the importance of prompt engineering and how it can dramatically improve your inference results, I learned to navigate the natural language processing (NLP) terminology a lot more, and I learned about types of question chain memory. I also learned that open-source models give the possibility to develop and deploy LLM applications to whoever is interested and puts in the time
to research the documentation and troubleshoot or workaround current issues.


## What's next for Dolly Expert Lite
- **Multi-lingual:** For the next iteration of Dolly Expert Lite, I would like to experiment and see if I can get as good results making vector stores using information in other languages and multi-lingual embeddings. That would enable the development of other non-common applications, not seen in tutorials or popular guides. For example, a legal aide to help in navigating the Labor Act of Mexico, or a regulatory compliance aide that can interpret Canadian French.
- **Performance:** To improve inference speed, I would like to look into fine-tuning Dolly for question answering and investigate if there is a method for quantization I could use to try and use the 12B or the 7B model while trying to maintain consistent, relatively short inference times. I am also interested in the [optimum](https://github.com/huggingface/optimum) library and would like to work on a use case for the [Intel Neural Stick](https://a.co/d/6SdhYIf), which could be an affordable alternative for local inference.
- **Memory:** As for new features, I would like to try using knowledge graph memory to store key items in conversations, enabling the use of the tools for more complex cases. For example, clarifying if a regulatory requirement has been met and if not, how the requirement could be broken down and described for its implementation.
