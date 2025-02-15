from typing import List
from domain.document.document_id import DocumentId
from domain.document.document_operation_response import DocumentOperationResponse

   
"""
This interface is the output port of the EnableDocumentsUseCase. It is used to enable the documents.
"""
class EnableDocumentsUseCase:
       
    """
    Enables the documents and returns the response.
    Args:
        documentsIds (List[DocumentId]): The documents to enable.
    Returns:
        List[DocumentOperationResponse]: The response of the operation.
    """ 
    def enableDocuments(self, documentsIds: List[DocumentId]) -> List[DocumentOperationResponse]:
        pass