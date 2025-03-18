import uuid
import pytest
from unittest.mock import patch, MagicMock

from src.db.models import User, Session
from src.db.repository import get_user_by_identifier, list_sessions

# Mock data
MOCK_USER_ID = 42
MOCK_USER_EMAIL = "test@example.com"
MOCK_USER_PHONE = "1234567890"
MOCK_USER_DATA = {"name": "Test User"}
MOCK_USER_ROW = {
    "id": MOCK_USER_ID,
    "email": MOCK_USER_EMAIL,
    "phone_number": MOCK_USER_PHONE,
    "user_data": MOCK_USER_DATA,
    "created_at": "2025-03-15T22:57:00",
    "updated_at": "2025-03-15T22:57:00"
}

MOCK_SESSION_ID = uuid.uuid4()
MOCK_SESSION_NAME = "test-session"
MOCK_SESSION_ROW = {
    "id": str(MOCK_SESSION_ID),
    "user_id": MOCK_USER_ID,
    "agent_id": 1,
    "name": MOCK_SESSION_NAME,
    "platform": "web",
    "metadata": {"test": "data"},
    "created_at": "2025-03-15T22:57:00",
    "updated_at": "2025-03-15T22:57:00",
    "run_finished_at": None
}

# Tests for get_user_by_identifier
@patch('src.db.repository.execute_query')
def test_get_user_by_identifier_with_id(mock_execute_query):
    # Setup
    mock_execute_query.return_value = [MOCK_USER_ROW]
    
    # Execute
    user = get_user_by_identifier(str(MOCK_USER_ID))
    
    # Assert
    assert user is not None
    assert user.id == MOCK_USER_ID
    assert user.email == MOCK_USER_EMAIL
    assert user.phone_number == MOCK_USER_PHONE
    assert user.user_data == MOCK_USER_DATA
    
    # Verify correct query was executed
    mock_execute_query.assert_called_once()
    args, _ = mock_execute_query.call_args
    assert "SELECT * FROM users WHERE id = %s" in args[0]

@patch('src.db.repository.execute_query')
def test_get_user_by_identifier_with_email(mock_execute_query):
    # Setup
    mock_execute_query.side_effect = [
        [],  # First call for ID lookup returns nothing
        [MOCK_USER_ROW]  # Second call for email lookup returns the user
    ]
    
    # Execute
    user = get_user_by_identifier(MOCK_USER_EMAIL)
    
    # Assert
    assert user is not None
    assert user.id == MOCK_USER_ID
    assert user.email == MOCK_USER_EMAIL
    
    # Verify correct queries were executed
    assert mock_execute_query.call_count == 2
    args, _ = mock_execute_query.call_args
    assert "SELECT * FROM users WHERE email = %s" in args[0]

@patch('src.db.repository.execute_query')
def test_get_user_by_identifier_with_phone(mock_execute_query):
    # Setup
    mock_execute_query.side_effect = [
        [],  # First call for ID lookup returns nothing
        [],  # Second call for email lookup returns nothing
        [MOCK_USER_ROW]  # Third call for phone lookup returns the user
    ]
    
    # Execute
    user = get_user_by_identifier(MOCK_USER_PHONE)
    
    # Assert
    assert user is not None
    assert user.id == MOCK_USER_ID
    assert user.phone_number == MOCK_USER_PHONE
    
    # Verify correct queries were executed
    assert mock_execute_query.call_count == 3
    args, _ = mock_execute_query.call_args
    assert "SELECT * FROM users WHERE phone_number = %s" in args[0]

@patch('src.db.repository.execute_query')
def test_get_user_by_identifier_not_found(mock_execute_query):
    # Setup
    mock_execute_query.return_value = []
    
    # Execute
    user = get_user_by_identifier("nonexistent")
    
    # Assert
    assert user is None
    
    # Verify correct queries were executed
    assert mock_execute_query.call_count >= 1

# Tests for list_sessions with pagination
@patch('src.db.repository.execute_query')
def test_list_sessions_with_pagination(mock_execute_query):
    # Setup
    mock_execute_query.side_effect = [
        [{"count": 10}],  # First call for count returns 10 total
        [MOCK_SESSION_ROW] * 5  # Second call returns 5 session rows
    ]
    
    # Execute
    sessions, total_count = list_sessions(page=1, page_size=5)
    
    # Assert
    assert total_count == 10
    assert len(sessions) == 5
    assert all(isinstance(session, Session) for session in sessions)
    assert sessions[0].id == MOCK_SESSION_ID
    assert sessions[0].name == MOCK_SESSION_NAME
    
    # Verify correct queries were executed
    assert mock_execute_query.call_count == 2
    
    # Verify pagination parameters
    pagination_call_args, _ = mock_execute_query.call_args
    assert "LIMIT %s OFFSET %s" in pagination_call_args[0]
    assert len(pagination_call_args[1]) == 2  # Should have parameters for LIMIT and OFFSET

@patch('src.db.repository.execute_query')
def test_list_sessions_with_filters(mock_execute_query):
    # Setup
    mock_execute_query.side_effect = [
        [{"count": 3}],  # First call for count returns 3 total
        [MOCK_SESSION_ROW] * 3  # Second call returns 3 session rows
    ]
    
    # Execute with filters
    sessions, total_count = list_sessions(
        user_id=MOCK_USER_ID,
        agent_id=1,
        page=1,
        page_size=10
    )
    
    # Assert
    assert total_count == 3
    assert len(sessions) == 3
    
    # Verify WHERE conditions for filters
    count_query_args, _ = mock_execute_query.call_args_list[0]
    assert "WHERE" in count_query_args[0]
    assert "user_id = %s" in count_query_args[0]
    assert "agent_id = %s" in count_query_args[0]

@patch('src.db.repository.execute_query')
def test_list_sessions_empty_result(mock_execute_query):
    # Setup
    mock_execute_query.side_effect = [
        [{"count": 0}],  # First call for count returns 0 total
        []  # Second call returns empty list
    ]
    
    # Execute
    sessions, total_count = list_sessions(page=1, page_size=10)
    
    # Assert
    assert total_count == 0
    assert len(sessions) == 0
    assert isinstance(sessions, list)

@patch('src.db.repository.execute_query')
def test_create_session_with_provided_uuid(mock_execute_query):
    # Setup
    session_id = uuid.uuid4()
    mock_execute_query.return_value = [{"id": str(session_id)}]
    
    # Create a session with a UUID already set
    from src.db.models import Session
    session = Session(
        id=session_id,
        user_id=1,
        agent_id=1,
        name="test-session",
        platform="web",
        metadata={"test": "data"}
    )
    
    # Execute
    from src.db.repository import create_session
    result_id = create_session(session)
    
    # Assert
    assert result_id == session_id
    
    # Verify the UUID was passed correctly to the query
    args, _ = mock_execute_query.call_args
    assert args[1][0] == str(session_id)  # First parameter should be the session ID

@patch('src.db.repository.execute_query')
def test_create_session_without_uuid(mock_execute_query):
    # Setup - mock a successful insert that returns the UUID that was generated
    result_uuid = uuid.uuid4()
    mock_execute_query.return_value = [{"id": str(result_uuid)}]
    
    # Create a session without a UUID
    from src.db.models import Session
    session = Session(
        user_id=1,
        agent_id=1,
        name="test-session-no-uuid",
        platform="web",
        metadata={"test": "data"}
    )
    
    # Execute
    from src.db.repository import create_session
    result_id = create_session(session)
    
    # Assert
    assert result_id is not None
    assert isinstance(result_id, uuid.UUID)
    
    # Verify a UUID was generated and passed to the query
    args, _ = mock_execute_query.call_args
    assert args[1][0] is not None  # First parameter should be the generated UUID
    assert len(str(args[1][0])) == 36  # UUID string length 