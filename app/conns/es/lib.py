import requests
import logging
import base64
import json
from aiohttp import ClientSession


logger = logging.getLogger(__name__)



class Methods():
    def __init__(self, base_url):
        self.base_url = base_url

    def create_index(self, index_name):
        return f"{self.base_url}/{index_name}"

    def get_index(self, index_name):
        return f"{self.base_url}/{index_name}"

    def delete_index(self, index_name):
        return f"{self.base_url}/{index_name}"

    def create_document(self, index_name):
        """create with auto generated id"""
        return f"{self.base_url}/{index_name}/_doc"

    def create_document_with_id(self, index_name, document_id):
        return f"{self.base_url}/{index_name}/_create/{document_id}"

    def create_or_update_document(self, index_name):
        return f"{self.base_url}/{index_name}/_doc"

    def create_or_update_document_with_id(self, index_name, document_id):
        return f"{self.base_url}/{index_name}/_doc/{document_id}"


    def bulk_create(self, index_name: str):
        return f"{self.base_url}/{index_name}/_bulk"

    def get_document(self, index_name, document_id):
        return f"{self.base_url}/{index_name}/_doc/{document_id}"

    def get_documents(self, index_name):
        return f"{self.base_url}/{index_name}/_mget"

    def delete_document(self, index_name, document_id):
        return f"{self.base_url}/{index_name}/_doc/{document_id}"

    def search(self, index_name):
        return f"{self.base_url}/{index_name}/_search"




class EsApi():
    """
    https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html
    """
    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.user = user
        self.password = password
        self.methods = Methods(base_url)


    @property
    def headers(self):
        """ with basic auth """
        auth_str = base64.b64encode(f'{self.user}:{self.password}'.encode()).decode()
        return {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': f"Basic {auth_str}"
        }

    def create_index(self, index_name: str, request_body: dict):
        response = requests.put(url=self.methods.create_index(index_name),
                                headers=self.headers,
                                json=request_body)
        return response.json()



    def get_index(self, index_name):
        response = requests.get(url=self.methods.get_index(index_name),
                                headers=self.headers)
        return response.json()


    def delete_index(self, index_name):
        response = requests.delete(url=self.methods.delete_index(index_name),
                                headers=self.headers)
        return response.json()


    def create_document(self, index_name, document):
        """Создание с автогенерацией id"""
        response = requests.post(url=self.methods.create_document(index_name=index_name),
                                headers=self.headers,
                                json=document)
        return response.json()



    def create_document_with_id(self, index_name, document_id, document):
        """Создание с явным указанием id"""
        response = requests.post(url=self.methods.create_document_with_id(index_name=index_name, document_id=document_id),
                                headers=self.headers,
                                json=document)
        return response.json()


    def create_or_update_document_with_id(self, index_name, document_id, document):
        """Обновление или создание"""
        response = requests.put(url=self.methods.create_or_update_document_with_id(index_name=index_name, document_id=document_id),
                                headers=self.headers,
                                json=document)
        return response.json()

    def create_or_update_document(self, index_name, document):
        """Обновление или создание"""
        response = requests.put(url=self.methods.create_or_update_document(index_name=index_name),
                                headers=self.headers,
                                json=document)
        return response.json()


    def bulk_create(self, index_name: str, data: list[dict]):
        """Создание пачкой"""
        rows = ""
        for doc in data:
            action_and_meta_data = json.dumps({"create": {"_index": index_name}}) + '\n'
            rows += action_and_meta_data
            optional_source = json.dumps(doc) + '\n'
            rows += optional_source
        response = requests.put(url=self.methods.bulk_create(index_name=index_name),
                                 headers=self.headers,
                                 data=rows)
        return response.json()


    def get_document(self, index_name, document_id):
        """Получение документа"""
        response = requests.get(url=self.methods.get_document(index_name=index_name, document_id=document_id),
                                headers=self.headers)
        return response.json()

    def get_documents(self, index_name: str, document_ids: list[str]):
        """Получение документов по списку id"""
        response = requests.get(url=self.methods.get_documents(index_name=index_name),
                                headers=self.headers,
                                json={"ids": document_ids})
        return response.json()

    def delete_document(self, index_name, document_id):
        response = requests.delete(url=self.methods.delete_document(index_name=index_name, document_id=document_id),
                                   headers=self.headers)
        return response.json()

    def search(self, index_name, query_params=None, request_body=None):
        if not request_body:
            request_body = dict()
        if not query_params:
            query_params = dict()

        response = requests.get(url=self.methods.search(index_name=index_name),
                                headers=self.headers,
                                json=request_body,
                                params=query_params)
        return response.json()
    
    
    
class AsyncEsApi(EsApi):
    async def create_document(self, index_name, document):
        async with ClientSession() as session:
            async with session.post(url=self.methods.create_document(index_name=index_name),
                                    headers=self.headers,
                                    json=document,
                                    timeout=10
                                   ) as response:
                return await response.json()