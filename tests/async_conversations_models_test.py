"""Tests for the ConversationsModels class."""

from __future__ import annotations

import os
import sys

import pytest

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_keys,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.conversations_models import ConversationsModels
from typesense.types.conversations_model import ConversationModelSchema


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the ConversationsModels object is initialized correctly."""
    conversations_models = ConversationsModels(fake_api_call_async)

    assert_match_object(conversations_models.api_call, fake_api_call_async)
    assert_object_lists_match(
        conversations_models.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        conversations_models.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )

    assert not conversations_models.conversations_models


def test_get_missing_conversations_model(
    fake_conversations_models_async: ConversationsModels,
) -> None:
    """Test that the ConversationsModels object can get a missing conversations_model."""
    conversations_model = fake_conversations_models_async["conversation_model_id"]

    assert_match_object(
        conversations_model.api_call,
        fake_conversations_models_async.api_call,
    )
    assert_object_lists_match(
        conversations_model.api_call.node_manager.nodes,
        fake_conversations_models_async.api_call.node_manager.nodes,
    )
    assert_match_object(
        conversations_model.api_call.config.nearest_node,
        fake_conversations_models_async.api_call.config.nearest_node,
    )
    assert (
        conversations_model._endpoint_path
        == "/conversations/models/conversation_model_id"
    )


def test_get_existing_conversations_model(
    fake_conversations_models_async: ConversationsModels,
) -> None:
    """Test that the ConversationsModels object can get an existing conversations_model."""
    conversations_model = fake_conversations_models_async["conversations_model_id"]
    fetched_conversations_model = fake_conversations_models_async[
        "conversations_model_id"
    ]

    assert len(fake_conversations_models_async.conversations_models) == 1

    assert conversations_model is fetched_conversations_model


@pytest.mark.asyncio
async def test_retrieve(
    fake_conversations_models_async: ConversationsModels, httpx_mock
) -> None:
    """Test that the ConversationsModels object can retrieve conversations_models."""
    json_response: typing.List[ConversationModelSchema] = [
        {
            "api_key": "abc",
            "id": "1",
            "max_bytes": 1000000,
            "model_name": "openAI-gpt-3",
            "system_prompt": "This is a system prompt",
        },
    ]

    httpx_mock.add_response(
        url="http://nearest:8108/conversations/models",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_conversations_models_async.retrieve()

    assert len(response) == 1
    assert response[0] == json_response[0]
    assert response == json_response


@pytest.mark.asyncio
async def test_create(
    fake_conversations_models_async: ConversationsModels, httpx_mock
) -> None:
    """Test that the ConversationsModels object can create a conversations_model."""
    json_response: ConversationModelSchema = {
        "api_key": "abc",
        "id": "1",
        "max_bytes": 1000000,
        "model_name": "openAI-gpt-3",
        "system_prompt": "This is a system prompt",
    }

    httpx_mock.add_response(
        url="http://nearest:8108/conversations/models",
        method="POST",
        json=json_response,
        status_code=201,
    )

    await fake_conversations_models_async.create(
        model={
            "api_key": "abc",
            "id": "1",
            "max_bytes": 1000000,
            "model_name": "openAI-gpt-3",
            "system_prompt": "This is a system prompt",
        },
    )

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "POST"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/conversations/models"
    )
    assert (
        httpx_mock.get_requests()[0].read().decode()
        == '{"api_key": "abc", "id": "1", "max_bytes": 1000000, "model_name": "openAI-gpt-3", "system_prompt": "This is a system prompt"}'
    )


@pytest.mark.open_ai
@pytest.mark.asyncio
async def test_actual_create(
    actual_conversations_models_async: ConversationsModels,
    create_conversation_history_collection_async: None,
) -> None:
    """Test that it can create an conversations_model on Typesense Server."""
    response = await actual_conversations_models_async.create(
        {
            "api_key": os.environ["OPEN_AI_KEY"],
            "history_collection": "conversation_store",
            "max_bytes": 16384,
            "model_name": "openai/gpt-3.5-turbo",
            "system_prompt": "This is meant for testing purposes",
        },
    )

    assert_to_contain_keys(
        response,
        ["id", "api_key", "max_bytes", "model_name", "system_prompt"],
    )


@pytest.mark.open_ai
@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_conversations_models_async: ConversationsModels,
    delete_all_async: None,
    delete_all_conversations_models_async: None,
    create_conversations_model_async: str,
) -> None:
    """Test that it can retrieve an conversations_model from Typesense Server."""
    response = await actual_conversations_models_async.retrieve()
    assert len(response) == 1
    assert_to_contain_object(
        response[0],
        {
            "id": create_conversations_model_async,
        },
    )
    assert_to_contain_keys(
        response[0],
        ["id", "api_key", "max_bytes", "model_name", "system_prompt"],
    )
