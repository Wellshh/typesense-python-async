"""Fixtures for the stopword tests."""

import httpx
import pytest
import pytest_asyncio
import requests

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.stopwords import Stopwords as AsyncStopwords
from typesense.async_client.stopwords_set import StopwordsSet as AsyncStopwordsSet
from typesense.stopwords import Stopwords
from typesense.stopwords_set import StopwordsSet


@pytest.fixture(scope="function", name="create_stopword")
def create_stopword_fixture() -> None:
    """Create a stopword set in the Typesense server."""
    url = "http://localhost:8108/stopwords/company_stopwords"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    stopword_data = {
        "stopwords": ["and", "is", "the"],
    }

    create_stopword_response = requests.put(
        url,
        headers=headers,
        json=stopword_data,
        timeout=3,
    )
    create_stopword_response.raise_for_status()


@pytest.fixture(scope="function", name="delete_all_stopwords")
def clear_typesense_stopwords() -> None:
    """Remove all stopwords from the Typesense server."""
    url = "http://localhost:8108/stopwords"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    # Get the list of stopwords
    response = requests.get(url, headers=headers, timeout=3)
    response.raise_for_status()
    stopwords = response.json()

    # Delete each stopword
    for stopword_set in stopwords["stopwords"]:
        stopword_id = stopword_set.get("id")
        delete_url = f"{url}/{stopword_id}"
        delete_response = requests.delete(delete_url, headers=headers, timeout=3)
        delete_response.raise_for_status()


@pytest.fixture(scope="function", name="actual_stopwords")
def actual_stopwords_fixture(actual_api_call: ApiCall) -> Stopwords:
    """Return a Stopwords object using a real API."""
    return Stopwords(actual_api_call)


@pytest.fixture(scope="function", name="actual_stopwords_set")
def actual_stopwords_set_fixture(actual_api_call: ApiCall) -> StopwordsSet:
    """Return a Stopwords object using a real API."""
    return StopwordsSet(actual_api_call, "company_stopwords")


@pytest.fixture(scope="function", name="fake_stopwords")
def fake_stopwords_fixture(fake_api_call: ApiCall) -> Stopwords:
    """Return a Stopwords object with test values."""
    return Stopwords(fake_api_call)


@pytest.fixture(scope="function", name="fake_stopwords_set")
def fake_stopwords_set_fixture(fake_api_call: ApiCall) -> StopwordsSet:
    """Return a Collection object with test values."""
    return StopwordsSet(fake_api_call, "company_stopwords")


@pytest_asyncio.fixture(loop_scope="function", name="create_stopword_async")
async def create_stopword_fixture_async() -> None:
    """Create a stopword set in the Typesense server asynchronously."""
    url = "http://localhost:8108/stopwords/company_stopwords"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    stopword_data = {
        "stopwords": ["and", "is", "the"],
    }

    async with httpx.AsyncClient() as client:
        create_stopword_response = await client.put(
            url,
            headers=headers,
            json=stopword_data,
            timeout=3,
        )
        create_stopword_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="delete_all_stopwords_async")
async def clear_typesense_stopwords_async() -> None:
    """Remove all stopwords from the Typesense server asynchronously."""
    url = "http://localhost:8108/stopwords"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        stopwords = response.json()

        for stopword_set in stopwords["stopwords"]:
            stopword_id = stopword_set.get("id")
            delete_url = f"{url}/{stopword_id}"
            delete_response = await client.delete(
                delete_url, headers=headers, timeout=3
            )
            delete_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="actual_stopwords_async")
async def actual_stopwords_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncStopwords:
    """Return an AsyncStopwords object using a real API."""
    return AsyncStopwords(actual_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="actual_stopwords_set_async")
async def actual_stopwords_set_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncStopwordsSet:
    """Return an AsyncStopwordsSet object using a real API."""
    return AsyncStopwordsSet(actual_api_call_async, "company_stopwords")


@pytest_asyncio.fixture(loop_scope="function", name="fake_stopwords_async")
async def fake_stopwords_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncStopwords:
    """Return an AsyncStopwords object with test values."""
    return AsyncStopwords(fake_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_stopwords_set_async")
async def fake_stopwords_set_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncStopwordsSet:
    """Return an AsyncStopwordsSet object with test values."""
    return AsyncStopwordsSet(fake_api_call_async, "company_stopwords")
