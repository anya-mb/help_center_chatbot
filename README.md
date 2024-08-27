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

### Relevant questions
<img width="606" alt="bill_assistant_demo" src="https://github.com/user-attachments/assets/24b60002-00ad-4695-90c7-6449fda011f4">

### Irrelevant questions
<img width="803" alt="non-relevant_question" src="https://github.com/user-attachments/assets/87224796-7be1-4f4c-970e-48554afffdde">

### Video demo

https://youtu.be/e8xNKpBgsY0


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

## Useful Information

To rebuild RAG:

```
cd src
python RAG_manager.py
```

To run QA in CLI:
```
cd src
python help_center_chatbot.py --question "Why is my gas bill so high?"
```

## Key Directories and Files:

`src/`: Source code for the chatbot, including configuration files, scripts for parsing data, building RAG and the main chatbot logic.

`data/chroma_db`: Contains Chroma RAG vector store.

`data/Bill_FAQs`: Contains the FAQs, parsed documents.

`data/RAG_evaluation_data`: Contains all the data used to evaluate RAG (test datasets of queries and answers).

`notebooks/`: Jupyter notebooks for experimenting with RAG, NEMO Guardrails and evaluating different RAG versions.

`logs/`: Stores log files for tracking the chatbot's operation.

`.env`: Environment variables configuration file.

`README.md`: This README file.

`requirements.txt`: List of Python dependencies needed to run the project.

## Jupyter Notebooks

`notebooks/llama_index.ipynb` - shows how to build vector store, load it and query with LlamaIndex

`notebooks/NEMO_guardrails.ipynb` - the implementation of NEMO Guardrails

`notebooks/RAGAS_evaluation_of_RAG_versions.ipynb` - the evaluation of different RAGs

`notebooks/company_Q&A_with_RAG.ipynb` - shows how to build vector store, load it and query with LangChain


## Solutions document

Feel free to read the solution description [here](https://docs.google.com/document/d/1CvTr9m5-FjpbXdKhm5NpUcTQryfe9TTVpPmWsrRq82Y/edit?usp=sharing)
