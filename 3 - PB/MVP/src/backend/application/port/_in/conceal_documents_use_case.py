from typing import List
from domain.document.document_id import DocumentId
from domain.document.document_operation_response import DocumentOperationResponse
"""
This interface is the output port of the ConcealDocumentsUseCase. It is used to conceal the documents.
"""
class ConcealDocumentsUseCase:
       
    """
    Conceals the documents and returns the response.
    Args:
        documentsIds (List[DocumentId]): The documents to conceal.
    Returns:
        List[DocumentOperationResponse]: The response of the operation.
    """ 
    def concealDocuments(self, documentsIds: List[DocumentId]) -> List[DocumentOperationResponse]:
        pass