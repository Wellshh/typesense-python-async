"""Fixtures for ApiCall tests."""

import pytest
import pytest_asyncio

from typesense.api_call import ApiCall
from typesense.configuration import Configuration
from typesense.async_client.async_api_call import AsyncApiCall


@pytest.fixture(scope="function", name="fake_api_call")
def fake_api_call_fixture(
    fake_config: Configuration,
) -> ApiCall:
    """Return an ApiCall object with test values."""
    return ApiCall(fake_config)


@pytest.fixture(scope="function", name="actual_api_call")
def actual_api_call_fixture(actual_config: Configuration) -> ApiCall:
    """Return an ApiCall object using a real API."""
    return ApiCall(actual_config)


@pytest_asyncio.fixture(loop_scope="function", name="fake_api_call_async")
async def fake_api_call_fixture_async(
    fake_config: Configuration,
) -> AsyncApiCall:
    """Return an AsyncApiCall object with test values."""
    return AsyncApiCall(fake_config)


@pytest_asyncio.fixture(loop_scope="function", name="actual_api_call_async")
async def actual_api_call_fixture_async(actual_config: Configuration) -> AsyncApiCall:
    """Return an AsyncApiCall object using a real API."""
    return AsyncApiCall(actual_config)
