"""Fixtures for the MultiSearch class."""

import pytest
import pytest_asyncio

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.multi_search import MultiSearch as AsyncMultiSearch
from typesense.multi_search import MultiSearch


@pytest.fixture(scope="function", name="actual_multi_search")
def actual_multi_search_fixture(actual_api_call: ApiCall) -> MultiSearch:
    """Return a MultiSearch object using a real API."""
    return MultiSearch(actual_api_call)


@pytest_asyncio.fixture(loop_scope="function", name="actual_multi_search_async")
async def actual_multi_search_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncMultiSearch:
    """Return an AsyncMultiSearch object using a real API."""
    return AsyncMultiSearch(actual_api_call_async)
