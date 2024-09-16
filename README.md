# RAG LLM service

This service acts as the core backend for a Question and Answer (Q&A) system, providing infrastructure to handle document retrieval, text processing, and intelligent response generation. The backend is responsible for managing uploaded documents, processing queries, and serving accurate responses based on the available data.

Following documents uploaded with first build:

- https://www.mnb.hu/letoltes/financial-stability-report-may-2024-en.pdf, 

- https://www.mnb.hu/letoltes/mnb-competitiveness-report-2022.pdf
- https://www.mnb.hu/letoltes/zo-ld-pe-nzu-gyi-jelente-s-2024-eng-webes.pdf

## Technologies Used
- LangChain: Powers the Retrieval-Augmented Generation (RAG) system by integrating document retrieval with language model capabilities.
- Chroma: Used as the vector database to efficiently store and retrieve document embeddings for the RAG system.
- FastAPI: A modern web framework for building the backend API, handling requests, and serving responses.
- OpenAI: Provides the language models used to generate intelligent and context-aware responses based on retrieved documents.

## Initial Setup

During the initial build of the service, a set of foundational documents are uploaded and indexed. These documents are essential for the Q&A system to start functioning effectively and include key resources that the system will reference to answer user queries.

By uploading and processing these documents during the first build, the service ensures it’s ready for immediate use, allowing users to interact with the Q&A system without delay.


## Requirements
- Docker
- OpenAI api key

## Installation
- Copy .env.sample to .env and replace OPENAI_API_KEY
- Application runs on port 8080, make sure it's not taken
- Run command:
```sh
make build-run
```

To stop the application run
```sh
make stop
```

First build can take some time, please make sure you see following logs before testing:
```sh
INFO:     Started server process [N]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```


## Usage
Visit:
http://localhost:8080/api/v1/docs 

Testing Request body:
```
{
  "query": "what's with Growth of the corporate loan portfolio?"
}
```

Response:
```
{
  "answer": generated text,
  "references: [
    {
      link: link to reference
      text: chunk text
      page: page number
    }
  ]
}
```

## Code structure & Architecture Overview
The application is built using the FastAPI framework, with its entry point located in app/api.py. The structure is organized to ensure clear separation of concerns and scalability, enabling efficient document processing and response generation.


- `app/apps:` This directory contains the core entities of the application. In the current implementation, it houses the generator component responsible for producing responses within the Retrieval-Augmented Generation (RAG) system. This modular design allows for the future expansion of additional services or entities as needed.
- `app/configuration:` This module handles the reading of configuration parameters and is crucial for initializing the RAG chain. It is responsible for initial appplication setup as well as for managing the download, preprocessing, and integration of files into the system. This ensures that the documents are properly prepared and indexed before they can be used to generate responses.


- `app/core:` Contains various helper modules that provide essential utilities for the application.
`preprocessor/documents/services.py:` This file defines the Preprocessor class, a key component responsible for cleaning and preparing documents. It ensures that all incoming documents are processed and formatted correctly, making them ready for efficient retrieval and response generation.

- `app/data:` A dedicated folder for storing raw documents. These documents are the source material used by the RAG system to generate answers. As new documents are uploaded or updated, they are placed in this directory before being processed by the system.
