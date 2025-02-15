import os
from application.port.out.get_configuration_options_port import GetConfigurationOptionsPort
from domain.configuration.configuration_options import ConfigurationOptions
from adapter.out.persistence.postgres.postgres_configuration_orm import PostgresConfigurationORM

"""
This class is the implementation of the GetConfigurationOptionsPort interface. It uses the PostgresConfigurationORM to get the configuration options.
"""
class GetConfigurationOptionsPostgres(GetConfigurationOptionsPort):
    def __init__(self, postgresConfigurationORM: PostgresConfigurationORM):
        self.postgresConfigurationORM = postgresConfigurationORM
    
    """
    Gets the configuration options and returns them.
    Returns:
        ConfigurationOptions: The configuration options.
    """
    def getConfigurationOptions(self) -> ConfigurationOptions:
        postgresConfigurationVectorStoreOptions = self.postgresConfigurationORM.getVectorStoreOptions()
        postgresConfigurationEmbeddingModelOptions = self.postgresConfigurationORM.getEmbeddingModelOptions()
        postgresConfigurationLLMModelOptions = self.postgresConfigurationORM.getLLMModelOptions()
        postgresConfigurationDocumentStoreOptions = self.postgresConfigurationORM.getDocumentStoreOptions()
        
        return ConfigurationOptions(
            vectorStoreOptions=[option.toVectorStoreConfiguration() for option in postgresConfigurationVectorStoreOptions],
            embeddingModelOptions=[option.toEmbeddingModelConfiguration() for option in postgresConfigurationEmbeddingModelOptions],
            LLMModelOptions=[option.toLLMModelConfiguration() for option in postgresConfigurationLLMModelOptions],
            documentStoreOptions=[option.toDocumentStoreConfiguration() for option in postgresConfigurationDocumentStoreOptions]
        )