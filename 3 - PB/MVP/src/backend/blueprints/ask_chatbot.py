from flask import request, Blueprint, jsonify
from adapter._in.web.ask_chatbot_controller import AskChatbotController
from application.service.ask_chatbot_service import AskChatbotService
from api_exceptions import InsufficientParameters, APIBadRequest, APIElaborationException
from adapter.out.persistence.postgres.postgres_configuration_orm import PostgresConfigurationORM
from adapter.out.persistence.postgres.postgres_chat_orm import PostgresChatORM

from adapter.out.configuration_manager import ConfigurationManager

from adapter.out.ask_chatbot.postgres_persist_chat import PostgresPersistChat

askChatbotBlueprint = Blueprint("askChatbot", __name__)

@askChatbotBlueprint.route("/askChatbot", methods=['POST'])
def askChatbot():
    userMessage = request.form.get('message')
    chatId = request.form.get('chatId')
    if userMessage is None:
        raise InsufficientParameters()
    if userMessage.strip() == "":
        raise APIBadRequest(f"Filtro '{userMessage}' non valido.")
    if not chatId.isdigit() or int(chatId) < 0:
        raise APIBadRequest(f"Chat id '{chatId}' non valido.")
    
    configurationManager = ConfigurationManager(postgresConfigurationORM=PostgresConfigurationORM())
    
    controller = AskChatbotController(
        AskChatbotService(
            configurationManager.getAskChatbotPort(),
            PostgresPersistChat(PostgresChatORM())
        )
    )
    
    chatbotResponse = controller.askChatbot(userMessage.strip(), int(chatId))
    
    if chatbotResponse is None:
        raise APIElaborationException("Errore nella generazione della risposta.")
    
    return jsonify({
        "status": chatbotResponse.status,
        "chatbotResponse": {
            "message": chatbotResponse.messageResponse.content,
            "timestamp": chatbotResponse.messageResponse.timestamp,
            "relevantDocuments": [relevantDocument.id for relevantDocument in chatbotResponse.messageResponse.relevantDocuments],
            "sender": chatbotResponse.messageResponse.sender.name
        } if chatbotResponse.messageResponse else None,
        "chatId": chatbotResponse.chatId.id})