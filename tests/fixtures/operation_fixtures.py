"""Fixtures for the Operations tests."""

import pytest
import pytest_asyncio

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.operations import Operations as AsyncOperations
from typesense.operations import Operations


@pytest.fixture(scope="function", name="actual_operations")
def actual_operations_fixture(actual_api_call: ApiCall) -> Operations:
    """Return a Operations object using a real API."""
    return Operations(actual_api_call)


@pytest.fixture(scope="function", name="fake_operations")
def fake_operations_fixture(fake_api_call: ApiCall) -> Operations:
    """Return a Collection object with test values."""
    return Operations(fake_api_call)


@pytest_asyncio.fixture(loop_scope="function", name="actual_operations_async")
async def actual_operations_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncOperations:
    """Return an AsyncOperations object using a real API."""
    return AsyncOperations(actual_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_operations_async")
async def fake_operations_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncOperations:
    """Return an AsyncOperations object with test values."""
    return AsyncOperations(fake_api_call_async)
