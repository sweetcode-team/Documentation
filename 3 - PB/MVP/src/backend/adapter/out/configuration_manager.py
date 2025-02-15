import os

from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

from application.port.out.documents_uploader_port import DocumentsUploaderPort
from application.port.out.embeddings_uploader_port import EmbeddingsUploaderPort
from application.port.out.delete_documents_port import DeleteDocumentsPort
from application.port.out.delete_embeddings_port import DeleteEmbeddingsPort
from application.port.out.conceal_documents_port import ConcealDocumentsPort
from application.port.out.enable_documents_port import EnableDocumentsPort
from application.port.out.get_documents_metadata_port import GetDocumentsMetadataPort
from application.port.out.get_documents_status_port import GetDocumentsStatusPort
from application.port.out.get_documents_content_port import GetDocumentsContentPort
from application.port.out.ask_chatbot_port import AskChatbotPort
 
from adapter.out.persistence.postgres.postgres_configuration_orm import PostgresConfigurationORM
from adapter.out.persistence.postgres.configuration_models import PostgresDocumentStoreType, PostgresVectorStoreType, PostgresLLMModelType, PostgresEmbeddingModelType
from adapter.out.persistence.vector_store.vector_store_chromaDB_manager import VectorStoreChromaDBManager
from adapter.out.persistence.vector_store.vector_store_pinecone_manager import VectorStorePineconeManager
from adapter.out.upload_documents.huggingface_embedding_model import HuggingFaceEmbeddingModel
from adapter.out.upload_documents.openai_embedding_model import OpenAIEmbeddingModel

from adapter.out.persistence.aws.AWS_manager import AWSS3Manager
from adapter.out.conceal_documents.conceal_documents_vector_store import ConcealDocumentsVectorStore
from adapter.out.delete_documents.delete_documents_AWSS3 import DeleteDocumentsAWSS3
from adapter.out.delete_documents.delete_embeddings_vector_store import DeleteEmbeddingsVectorStore
from adapter.out.upload_documents.embeddings_creator import EmbeddingsCreator
from adapter.out.upload_documents.embeddings_uploader_facade_langchain import EmbeddingsUploaderFacadeLangchain
from adapter.out.upload_documents.embeddings_uploader_vector_store import EmbeddingsUploaderVectorStore
from adapter.out.enable_documents.enable_documents_vector_store import EnableDocumentsVectorStore
from adapter.out.get_documents.get_documents_list_awss3 import GetDocumentsListAWSS3
from adapter.out.get_documents.get_documents_status_vector_store import GetDocumentsStatusVectorStore
from adapter.out.upload_documents.chunkerizer import Chunkerizer
from adapter.out.upload_documents.documents_uploader_AWSS3 import DocumentsUploaderAWSS3
from adapter.out.get_documents.get_documents_content_awss3 import GetDocumentsContentAWSS3
from adapter.out.ask_chatbot.ask_chatbot_langchain import AskChatbotLangchain
from adapter.out.persistence.postgres.chat_history_manager import ChatHistoryManager


   
class ConfigurationException(Exception):
    pass

"""
This class is the implementation of the ConfigurationManager interface. It uses the PostgresConfigurationORM to get the configuration and the other adapters to get the ports.
    Attributes:
        postgresConfigurationORM (PostgresConfigurationORM): The PostgresConfigurationORM to use to get the configuration.
"""        
class ConfigurationManager:
    def __init__(self, postgresConfigurationORM: PostgresConfigurationORM):
        self.postgresConfigurationORM = postgresConfigurationORM

   
    """
    Gets the DocumentsUploaderPort.
    Returns:
        DocumentsUploaderPort: The DocumentsUploaderPort.
    """ 
    def getDocumentsUploaderPort(self) -> DocumentsUploaderPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.documentStore == PostgresDocumentStoreType.AWS:
            configuredDocumentStore = DocumentsUploaderAWSS3(
                    AWSS3Manager()
                )
        else:
            raise ConfigurationException('Document store non configurato.')
        
        return configuredDocumentStore

   
    """
    Gets the EmbeddingsUploaderPort.
    Returns:
        EmbeddingsUploaderPort: The EmbeddingsUploaderPort.
    """ 
    def getEmbeddingsUploaderPort(self) -> EmbeddingsUploaderPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.vectorStore == PostgresVectorStoreType.PINECONE:
            configuredVectorStore = VectorStorePineconeManager()
        elif configuration.vectorStore == PostgresVectorStoreType.CHROMA_DB:
            configuredVectorStore = VectorStoreChromaDBManager()
        else:
            raise ConfigurationException('Vector store non configurato.')

        if configuration.embeddingModel == PostgresEmbeddingModelType.HUGGINGFACE:
            configuredEmbeddingModel = HuggingFaceEmbeddingModel()
        elif configuration.embeddingModel == PostgresEmbeddingModelType.OPENAI:
            configuredEmbeddingModel = OpenAIEmbeddingModel()
        else:
            raise ConfigurationException('Embeddings model non configurato.')
        
        return EmbeddingsUploaderFacadeLangchain(
                    Chunkerizer(),
                    EmbeddingsCreator(configuredEmbeddingModel),
                    EmbeddingsUploaderVectorStore(configuredVectorStore)
                )

   
    """
    Gets the GetDocumentsStatusPort.
    Returns:
        GetDocumentsStatusPort: The GetDocumentsStatusPort.
    """ 
    def getGetDocumentsStatusPort(self) -> GetDocumentsStatusPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.vectorStore == PostgresVectorStoreType.PINECONE:
            configuredVectorStore = VectorStorePineconeManager()
        elif configuration.vectorStore == PostgresVectorStoreType.CHROMA_DB:
            configuredVectorStore = VectorStoreChromaDBManager()
        else:
            raise ConfigurationException('Vector store non configurato.')
        
        return GetDocumentsStatusVectorStore(configuredVectorStore)

   
    """
    Gets the GetDocumentsMetadataPort.
    Returns:
        GetDocumentsMetadataPort: The GetDocumentsMetadataPort.
    """ 
    def getGetDocumentsMetadataPort(self) -> GetDocumentsMetadataPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.documentStore == PostgresDocumentStoreType.AWS:
            configuredDocumentStore = GetDocumentsListAWSS3(
                    AWSS3Manager()
                )
        else:
            raise ConfigurationException('Document store non configurato.')
        
        return configuredDocumentStore

   
    """
    Gets the DeleteDocumentsPort.
    Returns:
        DeleteDocumentsPort: The DeleteDocumentsPort.
    """ 
    def getDeleteDocumentsPort(self) -> DeleteDocumentsPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.documentStore == PostgresDocumentStoreType.AWS:
            configuredDocumentStore = DeleteDocumentsAWSS3(
                    AWSS3Manager()
                )
        else:
            raise ConfigurationException('Document store non configurato.')
        
        return configuredDocumentStore

   
    """
    Gets the DeleteEmbeddingsPort.
    Returns:
        DeleteEmbeddingsPort: The DeleteEmbeddingsPort.
    """ 
    def getDeleteEmbeddingsPort(self) -> DeleteEmbeddingsPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.vectorStore == PostgresVectorStoreType.PINECONE:
            configuredVectorStore = VectorStorePineconeManager()
        elif configuration.vectorStore == PostgresVectorStoreType.CHROMA_DB:
            configuredVectorStore = VectorStoreChromaDBManager()
        else:
            raise ConfigurationException('Vector store non configurato.')
        
        return DeleteEmbeddingsVectorStore(configuredVectorStore)

   
    """
    Gets the ConcealDocumentsPort.
    Returns:
        ConcealDocumentsPort: The ConcealDocumentsPort.
    """ 
    def getConcealDocumentsPort(self) -> ConcealDocumentsPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.vectorStore == PostgresVectorStoreType.PINECONE:
            configuredVectorStore = VectorStorePineconeManager()
        elif configuration.vectorStore == PostgresVectorStoreType.CHROMA_DB:
            configuredVectorStore = VectorStoreChromaDBManager()
        else:
            raise ConfigurationException('Vector store non configurato.')
        
        return ConcealDocumentsVectorStore(configuredVectorStore)

   
    """
    Gets the EnableDocumentsPort.
    Returns:
        EnableDocumentsPort: The EnableDocumentsPort.
    """ 
    def getEnableDocumentsPort(self) -> EnableDocumentsPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.vectorStore == PostgresVectorStoreType.PINECONE:
            configuredVectorStore = VectorStorePineconeManager()
        elif configuration.vectorStore == PostgresVectorStoreType.CHROMA_DB:
            configuredVectorStore = VectorStoreChromaDBManager()
        else:
            raise ConfigurationException('Vector store non configurato.')
        
        return EnableDocumentsVectorStore(configuredVectorStore)

   
    """
    Gets the GetDocumentsContentPort.
    Returns:
        GetDocumentsContentPort: The GetDocumentsContentPort.
    """ 
    def getGetDocumentsContentPort(self) -> GetDocumentsContentPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.documentStore == PostgresDocumentStoreType.AWS:
            configuredDocumentStore = GetDocumentsContentAWSS3(
                    AWSS3Manager()
                )
        else:
            raise ConfigurationException('Document store non configurato.')

        return configuredDocumentStore

   
    """
    Gets the AskChatbotPort.
    Returns:
        AskChatbotPort: The AskChatbotPort.
    """ 
    def getAskChatbotPort(self) -> AskChatbotPort:
        configuration = self.postgresConfigurationORM.getConfigurationChoices(os.environ.get('USER_ID'))
        if configuration.vectorStore == PostgresVectorStoreType.PINECONE:
            configuredVectorStore = VectorStorePineconeManager()
        elif configuration.vectorStore == PostgresVectorStoreType.CHROMA_DB:
            configuredVectorStore = VectorStoreChromaDBManager()
        else:
            raise ConfigurationException('Vector store non configurato.')
        
        if configuration.embeddingModel == PostgresEmbeddingModelType.HUGGINGFACE:
            configuredEmbeddingModel = HuggingFaceEmbeddingModel()
        elif configuration.embeddingModel == PostgresEmbeddingModelType.OPENAI:
            configuredEmbeddingModel = OpenAIEmbeddingModel()
        else:
            raise ConfigurationException('Embedding model non configurato.')
        
        if configuration.LLMModel == PostgresLLMModelType.OPENAI:
            with open('/run/secrets/openai_key', 'r') as file:
                openai_key = file.read()
            configuredLLMModel = OpenAI(openai_api_key=openai_key, model_name="gpt-3.5-turbo-instruct", temperature=0.3,)
        elif configuration.LLMModel == PostgresLLMModelType.HUGGINGFACE:
            with open('/run/secrets/huggingface_key', 'r') as file:
                hugging_face = file.read()
            configuredLLMModel = HuggingFaceEndpoint(repo_id="google/flan-t5-xxl", temperature=0.3, huggingfacehub_api_token=hugging_face)
        else:
            raise ConfigurationException('LLM model non configurato.')

        prompt = PromptTemplate(
            input_variables=["chat_history", "context", "question"],
            template="""Answer the question in your own words as truthfully as possible from the context given to you.\n
If you don't know the answer, just say that you don't know, don't try to make up an answer.\n
If questions are asked without relevant context, kindly request for questions pertinent to the documents and 
don't give suggestions that are not based on the context given to you.\n
If the answer you provide includes some specific informations, don't invent this information and instead just say that you don't know and kindly 
request for questions pertinent to the documents.\n
Always answer in Italian.
Chat History:
{chat_history}
Context:
{context}
Human: {question}
Assistant:"""
        )
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=configuredLLMModel,
            retriever=configuredVectorStore.getRetriever(configuredEmbeddingModel),
            return_source_documents=True,
            combine_docs_chain_kwargs={'prompt': prompt},
            verbose = True
        )
        return AskChatbotLangchain(chain=chain, chatHistoryManager=ChatHistoryManager())