import re
import requests
from typing import List
from pathlib import Path
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langchain.document_loaders import PyPDFLoader


class DocumentService:
    def __init__(self, document_links,  language='english', min_word_count=25) -> None:
        self.document_links = document_links
        self.pdf_files = self._download_documents(document_links)
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()
        self.min_word_count = min_word_count

    def _download_pdf(self, url: str, save_path: str):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Write the content of the response (which is the PDF file) to a local file
            with open(save_path, 'wb') as file:
                file.write(response.content)

            print(f"PDF downloaded successfully and saved as {save_path}")

            return save_path

        except requests.exceptions.RequestException as e:
            print(f"Failed to download PDF: {e}")

    def _download_documents(self, document_links):
        documents = []
        for name, link in document_links.items():
            save_path = self._download_pdf(link, f"app/data/{name}.pdf")
            documents.append(save_path)

        return documents

    def load_documents(self) -> List:
        """Download documents to file storage"""
        documents = []

        for pdf_file in self.pdf_files:
            loader = PyPDFLoader(pdf_file)
            loaded_docs = loader.load()
            documents.extend(loaded_docs)

        return documents

    def to_lowercase(self, text):
        """Convert all characters to lowercase."""
        return text.lower()

    def remove_special_characters(self, text):
        """Remove special characters, punctuation, and numbers."""
        return re.sub(r'[^a-zA-Z\s]', '', text)

    def remove_stopwords(self, text):
        """Remove stopwords from the text."""
        words = text.split()
        return ' '.join([word for word in words if word not in self.stop_words])

    def lemmatize_text(self, text):
        """Lemmatize each word in the text."""
        words = text.split()
        return ' '.join([self.lemmatizer.lemmatize(word) for word in words])

    def remove_extra_whitespace(self, text):
        """Remove extra whitespaces and newlines from the text."""
        return re.sub(r'\s+', ' ', text).strip()

    def clean_text(self, text):
        """Apply all cleaning methods in sequence."""
        text = self.to_lowercase(text)
        text = self.remove_special_characters(text)
        text = self.remove_stopwords(text)
        text = self.lemmatize_text(text)
        text = self.remove_extra_whitespace(text)
        return text

    def replace_source(self, path):
        file_name = Path(path).stem
        return self.document_links[file_name]

    def is_meaningful(self, text):
        """Check if the text has enough words to be considered a meaningful document."""
        words = text.split()
        if len(words) >= self.min_word_count:
            return True
        else:
            return False

    def clean_documents(self, documents):
        """Clean the list of Document objects in place by removing ones with insufficient content."""
        for i in range(len(documents) - 1, -1, -1):  # Iterate backwards
            if not self.is_meaningful(documents[i].page_content):
                # Remove document if it doesn't meet the criteria
                del documents[i]
            else:
                content = self.clean_text(documents[i].page_content)
                source = self.replace_source(documents[i].metadata["source"])
                documents[i].page_content = content
                documents[i].metadata["source"] = source

        return documents
