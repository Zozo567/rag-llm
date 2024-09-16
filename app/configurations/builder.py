import nltk
import json
from os import getenv
from typing import Union
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from app.core.models.environments import Stages
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.preprocessor.documents.services import DocumentService
from langchain.chains.combine_documents import create_stuff_documents_chain

nltk.download('stopwords')
nltk.download('wordnet')


class Parameters:
    """ Class which stands for managing application parameters stored in .env file """

    __stage_key_in_environment_file = 'STAGE'
    __document_links = 'DOCUMENT_LINKS'
    __openai_key = 'OPENAI_API_KEY'

    __available_stages = [stage.value for stage in Stages]

    def __init__(self) -> None:
        self.application_stage = getenv(
            self.__stage_key_in_environment_file, None
        )
        self.application_stage = None if self.application_stage is None else self.application_stage.lower()
        self.document_links = json.loads(getenv(self.__document_links, None))
        self.openai_key = getenv(self.__openai_key, None)

    def __check_environment_variables_not_none(self):
        environmnets = [
            self.openai_key,
            self.document_links,
            self.application_stage,
        ]

        if any(value is None for value in environmnets):
            raise EnvironmentError(
                f'Environmental variales are missing. Check: {environmnets}')
        return

    def __identify_stage_in_environment(self) -> Union[None, EnvironmentError]:
        try:
            self.application_stage = Stages(
                self.application_stage)     # Stages.production
            self.application_stage = self.application_stage.value       # production
            return

        except ValueError:
            message = f'Unsupported "STAGE" value {self.application_stage} provided in .env file. \
                        Supported stages: {self.__available_stages}'
            raise EnvironmentError(message)

    def __call__(self):
        self.__check_environment_variables_not_none()
        self.__identify_stage_in_environment()

        return {
            "stage": self.application_stage,
            "openai_key": self.openai_key,
            "document_links": self.document_links,
        }


class RAG:
    def __init__(self, parameters) -> None:
        self.document_links = parameters["document_links"]
        self.openai_key = parameters["openai_key"]

    def __call__(self):
        # Download documents and get their path
        document_service = DocumentService(self.document_links)
        documents = document_service.load_documents()

        # Clean up page content in documents
        cleaned_documents = document_service.clean_documents(documents)

        # Initialise llm model
        llm = ChatOpenAI(model="gpt-4o-mini")

        # Initialise text splitte (for chunking)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

        # Split loaded documents to chunks
        splits = text_splitter.split_documents(cleaned_documents)

        # Load data to vector store
        vectorstore = Chroma.from_documents(
            documents=splits, embedding=OpenAIEmbeddings()
        )

        # Initialise retriver
        retriever = vectorstore.as_retriever()

        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        return create_retrieval_chain(retriever, question_answer_chain)
