# Generative AI Chatbot for Electricity and Gas Customers
## Overview
This repository contains a Proof of Concept (PoC) for a chatbot designed to accurately and reliably answer customer queries related to Electricity and Gas using Generative AI technologies. The solution leverages advanced AI techniques to ensure that responses are both accurate and relevant, providing a solid foundation for future enhancements.

## Features
* **Generative AI Integration**: Utilizes state-of-the-art Generative AI technologies to provide truthful and accurate responses.
* **Efficient RAG System**: Built using LlamaIndex to create an efficient Retrieval Augmented Generation (RAG) system.
* **Guardrails for Safety**: Implements NEMO Guardrails to prevent jailbreak attempts and manage irrelevant, harmful, or inappropriate queries.
* **RAG Evaluation**: Employs the RAGAS approach to evaluate and select the optimal RAG version based on key metrics.
* **Vector Store**: Final RAG model is stored in Chroma Vector Store for efficient retrieval.
* **User Interface**: Developed with Streamlit for a user-friendly experience.

## Evaluation
The chatbot’s performance is evaluated using several metrics:

* **Faithfulness**: Consistency of the generated answer with the provided context.
* **Answer Relevancy**: Relevance of the answer to the given prompt.
* **Context Precision**: Accuracy of relevant items in the context.
* **Context Recall**: Alignment of retrieved context with the ground truth.
* **Harmfulness**: Safety and appropriateness of the responses.

## Demo usage



## Setup

Create virtual environment:

```
python -m venv venv
```

Activate the virtual environment:
* On Windows:
```
venv\Scripts\activate
```
* On macOS and Linux:

```
source venv/bin/activate
```

Add `OPENAI_API_KEY=` to `.env` file. See example in `.env_example` file.


## Run

To run streamlit frontend chatbot:
```
cd src
streamlit run app.py
```