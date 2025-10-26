"""Tests for the Debug class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import assert_match_object, assert_object_lists_match
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.debug import Debug
from typesense.types.debug import DebugResponseSchema


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Debug object is initialized correctly."""
    debug = Debug(
        fake_api_call_async,
    )

    assert_match_object(debug.api_call, fake_api_call_async)
    assert_object_lists_match(
        debug.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        debug.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert debug.resource_path == "/debug"


@pytest.mark.asyncio
async def test_retrieve(fake_debug_async: Debug, httpx_mock) -> None:
    """Test that the Debug object can retrieve a debug."""
    json_response: DebugResponseSchema = {"state": 1, "version": "27.1"}

    httpx_mock.add_response(
        url="http://nearest:8108/debug",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_debug_async.retrieve()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "GET"
    assert str(httpx_mock.get_requests()[0].url) == "http://nearest:8108/debug"
    assert response == json_response


@pytest.mark.asyncio
async def test_actual_retrieve(actual_debug_async: Debug) -> None:
    """Test that the Debug object can retrieve a debug on Typesense server and verify response structure."""
    response = await actual_debug_async.retrieve()

    assert "state" in response
    assert "version" in response

    assert isinstance(response["state"], int)
    assert isinstance(response["version"], str)
