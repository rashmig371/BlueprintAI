from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os

class KnowledgeBaseManager:
    def __init__(self):
        self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.search_key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = "project-planning-index"
        self.index_client = SearchIndexClient(endpoint=self.search_endpoint, credential=AzureKeyCredential(self.search_key))
        self.search_client = SearchClient(endpoint=self.search_endpoint, index_name=self.index_name, credential=AzureKeyCredential(self.search_key))

    def create_index_if_not_exists(self):
        # Define the index schema
        fields = [
            SimpleField(name="id", type="Edm.String", key=True),
            SearchableField(name="content", type="Edm.String")
        ]
        index = SearchIndex(name=self.index_name, fields=fields)
        # Create index if it doesn't exist
        try:
            self.index_client.get_index(self.index_name)
        except Exception:
            self.index_client.create_index(index)

    def upload_document(self, doc_id: str, text: str):
        self.create_index_if_not_exists()
        document = {"id": doc_id, "content": text}
        result = self.search_client.upload_documents(documents=[document])
        return result

    def search(self, query: str):
        results = self.search_client.search(query)
        return [doc["content"] for doc in results]