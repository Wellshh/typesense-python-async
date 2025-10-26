"""Fixtures for the Debug class tests."""

import pytest
import pytest_asyncio

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.debug import Debug as AsyncDebug
from typesense.debug import Debug


@pytest.fixture(scope="function", name="actual_debug")
def actual_debug_fixture(actual_api_call: ApiCall) -> Debug:
    """Return a Debug object using a real API."""
    return Debug(actual_api_call)


@pytest.fixture(scope="function", name="fake_debug")
def fake_debug_fixture(fake_api_call: ApiCall) -> Debug:
    """Return a debug object with test values."""
    return Debug(fake_api_call)


@pytest_asyncio.fixture(loop_scope="function", name="actual_debug_async")
async def actual_debug_fixture_async(actual_api_call_async: AsyncApiCall) -> AsyncDebug:
    """Return an AsyncDebug object using a real API."""
    return AsyncDebug(actual_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_debug_async")
async def fake_debug_fixture_async(fake_api_call_async: AsyncApiCall) -> AsyncDebug:
    """Return an AsyncDebug object with test values."""
    return AsyncDebug(fake_api_call_async)
