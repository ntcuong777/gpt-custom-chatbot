import os
import openai
from application.main.database.sql.schemas import ChatDialogueCreate
from application.main.database.sql import models
from application.main.database.sql import crud
from sqlalchemy.orm import Session
from common.logging import LoggerInstance
from application.main.strategy.doc_qa import AbstractDocQAProcessorStrategy, SimpleDocQAProcessorStrategy

from .base_service import BaseService

openai.api_key = os.environ["OPENAI_API_KEY"]
logger = LoggerInstance().get_logger(__name__)


class DocumentQuestionAnsweringService(BaseService):
    doc_qa_processor_strategy: AbstractDocQAProcessorStrategy = None

    def __init__(self, doc_qa_processor_strategy) -> None:
        self.doc_qa_processor_strategy = doc_qa_processor_strategy

    def save_doc(self, db: Session, session_id: str, doc_content: str):
        # TODO: implement
        pass

    def __save_user_dialouge(self, db: Session, session_id: str, user_input: str):
        user_dialogue = ChatDialogueCreate(session_id=session_id, role="user", content=user_input)
        return crud.ChatDialogueCrud.create_chat_dialogue(db, user_dialogue)

    def __save_assistant_response(self, db: Session, session_id: str, assistant_response: str) -> models.ChatDialogue:
        assistant_dialogue = ChatDialogueCreate(session_id=session_id, role="assistant", content=assistant_response)
        return crud.ChatDialogueCrud.create_chat_dialogue(db, assistant_dialogue)

    def __construct_message_prompt(self, referenced_doc: str, question: str):
        user_prompt = None # TODO: construct message prompt here

        messages = [
            {"role": "system", "content": "<Instruction for ChatGPT here>"},
            {"role": "user", "content": user_prompt}
        ]
        return messages

    def get_assistant_response(self, db: Session, model: str, session_id: str, question: str) -> str:
        referened_doc = self.doc_qa_processor_strategy.construct_referenced_doc_for_question(
            db, session_id=session_id, question=question)

        messages = self.__construct_message_prompt(referenced_doc=referened_doc, question=question)
        self.__save_user_dialouge(db, session_id=session_id, user_input=messages[1]["content"])

        response = openai.ChatCompletion.create(model=model, messages=messages)
        assistant_response = response["choices"][0]["message"]["content"]

        self.__save_assistant_response(db, session_id=session_id, assistant_response=assistant_response)

        return assistant_response


# Dependency
def get_document_question_answering_service():
    # Initialize service with corresponding strategy
    return DocumentQuestionAnsweringService(SimpleDocQAProcessorStrategy())
