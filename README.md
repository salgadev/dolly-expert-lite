---
title: dolly-expert-builder
app_file: app.py
sdk: gradio
sdk_version: 3.34.0
---
# dolly-expert-lite
Submission to the "So you think you can hack": open-source LLMs (e.g., OpenAssistant, MPT, Dolly, etc.) DevPost Hackathon.

# Inspiration
## Expert systems
 [Expert Systems](https://en.wikipedia.org/wiki/Expert_system) used to be big in artificial intelligence. They mimic the decision-making capabilities of a human expert in a particular field and can provide substantial value in many use cases. The main drawback of old school expert systems was that they had to be programmed using Boolean statements or a similar logic, taking considerable time and resources. In many occasions, this approach defeated the purpose of having a readily available expert for the task at hand.

## Closed-source LLMs
Closed-source LLM applications like ChatGPT3.5 and ChatGPT-4 are gigantic models that are very good a large number of tasks. They do have limitations such as hallucinations when they don't know how to respond or when the answer is online and they don't have access to the internet or files. Some times, these hallucinations will be told in very convincing ways and whenever one tries to implement them they will turn out to be flat-out false or incorrect. These models have enormous context windows so people can help them do
whatever task they struggle with by providing lots of information and implementing prompt engineering techniques. This makes more than one think that only the big companies with closed source code can develop and deploy LLM applications.

# What it does
Dolly Expert Lite leverages [dolly-v2-3b](dolly-v2-3b), the lightweight version of [dolly-v2-12b](https://huggingface.co/databricks/dolly-v2-12b), an open-source large language model ([LLM](https://en.wikipedia.org/wiki/Large_language_model)) to answer domain-specific questions using retrieval in custom-made vector databases. In this example deployment, [dolly-expert-builder](https://huggingface.co/spaces/salgadev/dolly-expert-builder) retrieves information from the [Ontario (Canada) building code](https://www.buildingcode.online/) to answer specific questions about construction, plumbing, electrical wiring and ventilation as per the official government code. [dolly-expert-builder](https://huggingface.co/spaces/salgadev/dolly-expert-builder) can provide coherent and factually correct information with sources and can serve as guidance suitable for tradespeople (plumbers, electricians, mechanics, home builders) as well as engineers and architects to aid in regulatory compliance while performing work.


# How we built it
- Model: [dolly-v2-3b](dolly-v2-3b) to exemplify lightweight development and deployment
- Framework: [LangChain](https://github.com/hwchase17/langchain) to make  the question answering chain and because of its integration with ChromaDB
- Text Embeddings: [Text Embeddings by Weakly-Supervised Contrastive Pre-training (E5-base-v2)](https://huggingface.co/intfloat/e5-base-v2). Because of their high score in retrieval tasks as per the [MTEB English Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [The Ontario (Canada) Building Code](https://www.buildingcode.online/): To make an example of how non-tech workers can benefit from LLM applications. The code page is not easy to navigate because the sections are just named "Section 1", "Section 2"..., "Section 14". Used their website to parse and convert into the vector store.
- Vector Store: [ChromaDB](https://github.com/chroma-core/chroma)
- Deployment: [HuggingFace Spaces](https://huggingface.co/) and [gradio](https://gradio.app/). Deployment available here: [Dolly Expert Builder](https://huggingface.co/spaces/salgadev/dolly-expert-builder)


# Challenges we ran into
Since the tools are so new, some divergences from the standard use cases cause errors. For example:
- Failure to use memory and sources in the same question answering chain in LangChain. A workaround was implemented by creating a class that inherited from the memory class.
- Error when web scrapping using sitemaps while on a Jupyter Notebook.  This could be circumvented applying the nest_asyncio workaround.
- Vector database not loading. Another early development LangChain issue, it saved partially when using ```persists_directory``` in the ChromaDB initialization and it would not load later in a separate instance because the .persists() method was not called. This had to be redone and committed again for the database to be finally available.
- Gradio app not launching on Jupyter Notebook. The previous workaround changed the local installation of asyncio, which is a Gradio requirement, making it unusable during the same runtime. To avoid this, the vector database was made in a separate notebook and committed to the repo.


# Accomplishments that we're proud of
TBC
We are proud of several accomplishments achieved with Dolly Expert Lite. Firstly, we successfully created a lightweight assistant that combines the power of the Dolly-v2 model with domain-specific question answering capabilities. This integration resulted in an accurate and efficient solution for users seeking expert knowledge. Additionally, we developed robust vector databases and implemented effective similarity searching algorithms, enhancing the system's ability to retrieve precise information. Overall, we take pride in delivering a high-quality and user-friendly experience through Dolly Expert Lite.

# What we learned
During the development of Dolly Expert Lite, we gained valuable insights into the intricacies of integrating state-of-the-art language models and building expert systems. We deepened our understanding of vector databases, similarity searching techniques, and how they can be harnessed to improve question answering systems. We also refined our skills in training and fine-tuning models, optimizing performance, and addressing challenges specific to working with large language models. These lessons will undoubtedly contribute to our future projects and endeavors.

# What's next for Dolly Expert Lite
Moving forward, we have exciting plans for Dolly Expert Lite. We aim to further enhance the assistant's capabilities by incorporating additional domain-specific knowledge and expanding the range of questions it can handle. We also intend to refine the conversational abilities of the assistant, making interactions even more natural and engaging. Continual improvement, user feedback integration, and exploring opportunities for integration with other platforms and technologies are key aspects of our roadmap for Dolly Expert Lite's future.
