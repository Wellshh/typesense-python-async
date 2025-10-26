"""Tests for the ConversationModel class."""

from __future__ import annotations

import pytest
from dotenv import load_dotenv

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_keys,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.conversation_model import ConversationModel
from typesense.async_client.conversations_models import ConversationsModels
from typesense.types.conversations_model import (
    ConversationModelDeleteSchema,
    ConversationModelSchema,
)

load_dotenv()


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the ConversationModel object is initialized correctly."""
    conversation_model = ConversationModel(
        fake_api_call_async,
        "conversation_model_id",
    )

    assert conversation_model.model_id == "conversation_model_id"
    assert_match_object(conversation_model.api_call, fake_api_call_async)
    assert_object_lists_match(
        conversation_model.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        conversation_model.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert (
        conversation_model._endpoint_path
        == "/conversations/models/conversation_model_id"
    )


@pytest.mark.asyncio
async def test_retrieve(
    fake_conversation_model_async: ConversationModel, httpx_mock
) -> None:
    """Test that the ConversationModel object can retrieve a conversation_model."""
    json_response: ConversationModelSchema = {
        "api_key": "abc",
        "id": "conversation_model_id",
        "max_bytes": 1000000,
        "model_name": "conversation_model_name",
        "system_prompt": "This is a system prompt",
    }

    httpx_mock.add_response(
        url="http://nearest:8108/conversations/models/conversation_model_id",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_conversation_model_async.retrieve()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "GET"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/conversations/models/conversation_model_id"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_delete(
    fake_conversation_model_async: ConversationModel, httpx_mock
) -> None:
    """Test that the ConversationModel object can delete a conversation_model."""
    json_response: ConversationModelDeleteSchema = {
        "id": "conversation_model_id",
    }
    httpx_mock.add_response(
        url="http://nearest:8108/conversations/models/conversation_model_id",
        method="DELETE",
        json=json_response,
        status_code=200,
    )

    response = await fake_conversation_model_async.delete()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "DELETE"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/conversations/models/conversation_model_id"
    )
    assert response == json_response


@pytest.mark.open_ai
@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_conversations_models_async: ConversationsModels,
    delete_all_conversations_models_async: None,
    create_conversations_model_async: str,
) -> None:
    """Test it can retrieve a conversation_model from Typesense Server."""
    response = await actual_conversations_models_async[
        create_conversations_model_async
    ].retrieve()

    assert_to_contain_keys(
        response,
        ["id", "model_name", "system_prompt", "max_bytes", "api_key"],
    )
    assert response.get("id") == create_conversations_model_async


@pytest.mark.open_ai
@pytest.mark.asyncio
async def test_actual_update(
    actual_conversations_models_async: ConversationsModels,
    delete_all_conversations_models_async: None,
    create_conversations_model_async: str,
) -> None:
    """Test that it can update a conversation_model from Typesense Server."""
    response = await actual_conversations_models_async[
        create_conversations_model_async
    ].update(
        {"system_prompt": "This is a new system prompt"},
    )

    assert_to_contain_keys(
        response,
        [
            "id",
            "model_name",
            "system_prompt",
            "max_bytes",
            "api_key",
            "ttl",
            "history_collection",
        ],
    )

    assert response.get("system_prompt") == "This is a new system prompt"
    assert response.get("id") == create_conversations_model_async


@pytest.mark.open_ai
@pytest.mark.asyncio
async def test_actual_delete(
    actual_conversations_models_async: ConversationsModels,
    delete_all_conversations_models_async: None,
    create_conversations_model_async: str,
) -> None:
    """Test that it can delete an conversation_model from Typesense Server."""
    response = await actual_conversations_models_async[
        create_conversations_model_async
    ].delete()

    assert_to_contain_keys(
        response,
        [
            "id",
            "model_name",
            "system_prompt",
            "max_bytes",
            "api_key",
            "ttl",
            "history_collection",
        ],
    )

    assert response.get("system_prompt") == "This is a system prompt"
    assert response.get("id") == create_conversations_model_async
    assert response.get("id") == create_conversations_model_async
