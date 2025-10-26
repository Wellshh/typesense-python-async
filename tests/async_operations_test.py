"""Tests for the Operations class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import assert_match_object, assert_object_lists_match
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.operations import Operations
from typesense.exceptions import ObjectNotFound


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Override object is initialized correctly."""
    operations = Operations(fake_api_call_async)

    assert_match_object(operations.api_call, fake_api_call_async)
    assert_object_lists_match(
        operations.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        operations.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert operations._endpoint_path("resource") == "/operations/resource"


@pytest.mark.asyncio
async def test_vote(actual_operations_async: Operations) -> None:
    """Test that the Operations object can perform the vote operation."""
    response = await actual_operations_async.perform("vote")

    # It will error on single node clusters if asserted to True
    assert response["success"] is not None


@pytest.mark.asyncio
async def test_db_compact(actual_operations_async: Operations) -> None:
    """Test that the Operations object can perform the db/compact operation."""
    response = await actual_operations_async.perform("db/compact")

    assert response["success"]


@pytest.mark.asyncio
async def test_cache_clear(actual_operations_async: Operations) -> None:
    """Test that the Operations object can perform the cache/clear operation."""
    response = await actual_operations_async.perform("cache/clear")

    assert response["success"]


@pytest.mark.asyncio
async def test_snapshot(actual_operations_async: Operations) -> None:
    """Test that the Operations object can perform the snapshot operation."""
    response = await actual_operations_async.perform(
        "snapshot",
        {"snapshot_path": "/tmp"},  # noqa: S108
    )

    assert response["success"]


@pytest.mark.asyncio
async def test_health(actual_operations_async: Operations) -> None:
    """Test that the Operations object can perform the health operation."""
    response = await actual_operations_async.is_healthy()

    assert response


@pytest.mark.asyncio
async def test_health_not_dict(fake_operations_async: Operations, httpx_mock) -> None:
    """Test that the Operations object can perform the health operation."""
    httpx_mock.add_response(
        url="http://nearest:8108/health",
        method="GET",
        json="ok",
        status_code=200,
    )

    response = await fake_operations_async.is_healthy()
    assert not response


@pytest.mark.asyncio
async def test_log_slow_requests_time_ms(actual_operations_async: Operations) -> None:
    """Test that the Operations object can perform the log_slow_requests_time_ms operation."""
    response = await actual_operations_async.toggle_slow_request_log(
        {"log_slow_requests_time_ms": 100},
    )

    assert response["success"]


@pytest.mark.asyncio
async def test_invalid_operation(actual_operations_async: Operations) -> None:
    """Test that the Operations object throws an error for an invalid operation."""
    with pytest.raises(ObjectNotFound):
        await actual_operations_async.perform("invalid")
