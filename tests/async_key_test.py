"""Tests for the Key class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.key import Key
from typesense.async_client.keys import Keys
from typesense.types.key import ApiKeyDeleteSchema, ApiKeySchema


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Key object is initialized correctly."""
    key = Key(fake_api_call_async, 3)

    assert key.key_id == 3
    assert_match_object(key.api_call, fake_api_call_async)
    assert_object_lists_match(
        key.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        key.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert key._endpoint_path == "/keys/3"


@pytest.mark.asyncio
async def test_retrieve(fake_key_async: Key, httpx_mock) -> None:
    """Test that the Key object can retrieve an key."""
    json_response: ApiKeySchema = {
        "actions": ["documents:search"],
        "collections": ["companies"],
        "description": "Search-only key",
    }

    httpx_mock.add_response(
        url="http://nearest:8108/keys/1",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_key_async.retrieve()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "GET"
    assert str(httpx_mock.get_requests()[0].url) == "http://nearest:8108/keys/1"
    assert response == json_response


@pytest.mark.asyncio
async def test_delete(fake_key_async: Key, httpx_mock) -> None:
    """Test that the Key object can delete an key."""
    json_response: ApiKeyDeleteSchema = {"id": 1}
    httpx_mock.add_response(
        url="http://nearest:8108/keys/1",
        method="DELETE",
        json=json_response,
        status_code=200,
    )

    response = await fake_key_async.delete()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "DELETE"
    assert str(httpx_mock.get_requests()[0].url) == "http://nearest:8108/keys/1"
    assert response == json_response


@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_keys_async: Keys,
    delete_all_keys_async: None,
    delete_all_async: None,
    create_key_id_async: int,
) -> None:
    """Test that the Key object can retrieve an key from Typesense Server."""
    response = await actual_keys_async[create_key_id_async].retrieve()

    assert_to_contain_object(
        response,
        {
            "actions": ["documents:search"],
            "collections": ["companies"],
            "description": "Search-only key",
            "id": create_key_id_async,
        },
    )


@pytest.mark.asyncio
async def test_actual_delete(
    actual_keys_async: Keys,
    delete_all_keys_async: None,
    delete_all_async: None,
    create_key_id_async: int,
) -> None:
    """Test that the Key object can delete an key from Typesense Server."""
    response = await actual_keys_async[create_key_id_async].delete()

    assert response == {"id": create_key_id_async}
