import ast
import openai
import functools
from typing import List
from abc import ABC, abstractmethod
from application.initializer import LoggerInstance
from sqlalchemy.orm import Session
from application.main.database.sql import crud
from application.main.decorator import overrides
from scipy import spatial  # for calculating vector similarities for search


logger = LoggerInstance().get_logger(__name__)

class AbstractDocQAProcessorStrategy(ABC):
    """
    Using strategy pattern to make future app extension easier for document QA ChatGPT API.
    """
    @abstractmethod
    def save_referenced_doc(self, db: Session, session_id: str, doc_content: str) -> str:
        raise NotImplementedError()


    @abstractmethod
    def construct_referenced_doc_for_question(self, db: Session, session_id: str, question: str) -> str:
        raise NotImplementedError()


class SimpleDocQAProcessorStrategy(AbstractDocQAProcessorStrategy):
    @overrides(AbstractDocQAProcessorStrategy)
    def save_referenced_doc(self, db: Session, session_id: str, doc_content: str) -> str:
        # TODO: save doc_content to database
        pass


    @overrides(AbstractDocQAProcessorStrategy)
    def construct_referenced_doc_for_question(self, db: Session, session_id: str, question: str) -> str:
        # Simply get document from database and return as-is
        doc = crud.DocumentCrud.fetch_single_document_given_session_id(db, session_id).doc_content
        return doc


# TODO: Add feature to search for top-k relevant text part for answering user query on larger documents
class TopKRelevantDocQAProcessorStrategy(AbstractDocQAProcessorStrategy):
    def __init__(self):
        self.top_k = 5


    @overrides(AbstractDocQAProcessorStrategy)
    def save_referenced_doc(self, db: Session, session_id: str, doc_content: str) -> str:
        # TODO: save doc_content to database and initialize embeddings by splitting doc_content
        pass


    # search function
    def __embeddings_ranked_by_relatedness(
        self,
        query_embedding: str,
        doc_parts: List[str],
        doc_part_idxs: List[int],
        doc_embeddings: List[float],
        relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    ) -> tuple[list[str], list[float]]:
        """Returns a list of indices of document embeddings and relatednesses, sorted from most related to least."""
        index_text_and_relatednesses = [
            (idx, text, relatedness_fn(query_embedding, doc_embed))
            for idx, text, doc_embed in zip(doc_part_idxs, doc_parts, doc_embeddings)
        ]

        index_text_and_relatednesses.sort(key=lambda x: x[2], reverse=True) # sort desc by relatedness
        indices, texts, relatednesses = zip(*index_text_and_relatednesses)

        return indices[:self.top_k], texts[:self.top_k], relatednesses[:self.top_k]


    @overrides(AbstractDocQAProcessorStrategy)
    def construct_referenced_doc(self, db: Session, session_id: str, question: str) -> str:
        question_embeddings = [] # TODO: request `question` embeddings from OpenAI

        doc = crud.DocumentCrud.fetch_single_document_given_session_id_eagerly_fetch_embeddings(db, session_id)
        doc_parts = [embedding.doc_part for embedding in doc.embeddings]
        doc_part_idxs = [embedding.doc_idx for embedding in doc.embeddings]
        doc_embeddings = [ast.literal_eval(embedding.embedding_vector) for embedding in doc.embeddings]

        index_text_and_relatedness = self.__embeddings_ranked_by_relatedness(question_embeddings, doc_parts, doc_part_idxs, doc_embeddings)
        index_text_and_relatedness.sort(key=lambda x: x[0])
        return functools.reduce(lambda doc, e: doc + "\n\n" + e[1], index_text_and_relatedness, "")
