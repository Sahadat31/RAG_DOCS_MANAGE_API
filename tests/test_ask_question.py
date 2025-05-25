from unittest.mock import patch, MagicMock
from app.services.ask_query import question

@patch("app.services.ask_query.question.users_collection.find_one")
@patch("app.services.ask_query.question.docs_mapper_collection.find_one")
@patch("app.services.ask_query.question.embedded_collection.find")
@patch("app.services.ask_query.question.FAISS.from_texts")
def test_answer_query_success(mock_faiss, mock_find, mock_mapper, mock_user):
    mock_user.return_value = {
        "_id": "user123",
        "embeddingsProcessed": ["doc_map_1"]
    }
    mock_mapper.return_value = {
        "embeddings": ["emb1", "emb2"]
    }
    mock_find.return_value = [
        {"text": "content 1", "metadata": {}, "document_id": "emb1"},
        {"text": "content 2", "metadata": {}, "document_id": "emb2"}
    ]
    mock_chain = MagicMock()
    mock_chain.run.return_value = "Mock answer"
    mock_faiss.return_value.as_retriever.return_value = MagicMock()
    with patch("app.services.ask_query.question.ChatGoogleGenerativeAI", return_value=MagicMock()), \
         patch("app.services.ask_query.question.RetrievalQA.from_chain_type", return_value=mock_chain):
        result = question.answer_query("What's up?", "user123")
        assert result == "Mock answer"
