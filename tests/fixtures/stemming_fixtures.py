"""Fixtures for the Analytics Rules tests."""

import pytest
import pytest_asyncio

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.stemming import Stemming as AsyncStemming
from typesense.stemming import Stemming


@pytest.fixture(scope="function", name="actual_stemming")
def actual_stemming_fixture(
    actual_api_call: ApiCall,
) -> Stemming:
    """Return a Stemming object using a real API."""
    return Stemming(actual_api_call)


@pytest_asyncio.fixture(loop_scope="function", name="actual_stemming_async")
async def actual_stemming_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncStemming:
    """Return an AsyncStemming object using a real API."""
    return AsyncStemming(actual_api_call_async)
