"""Fixtures for the synonym tests."""

import httpx
import pytest
import pytest_asyncio
import requests

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.synonym import Synonym as AsyncSynonym
from typesense.async_client.synonyms import Synonyms as AsyncSynonyms
from typesense.synonym import Synonym
from typesense.synonyms import Synonyms


@pytest.fixture(scope="function", name="create_synonym")
def create_synonym_fixture(create_collection: None) -> None:
    """Create a synonym in the Typesense server."""
    url = "http://localhost:8108/collections/companies/synonyms/company_synonym"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    synonym_data = {
        "synonyms": ["companies", "corporations", "firms"],
    }

    create_synonym_response = requests.put(
        url,
        headers=headers,
        json=synonym_data,
        timeout=3,
    )
    create_synonym_response.raise_for_status()


@pytest.fixture(scope="function", name="fake_synonyms")
def fake_synonyms_fixture(fake_api_call: ApiCall) -> Synonyms:
    """Return a Synonyms object with test values."""
    return Synonyms(fake_api_call, "companies")


@pytest.fixture(scope="function", name="actual_synonyms")
def actual_synonyms_fixture(actual_api_call: ApiCall) -> Synonyms:
    """Return a Synonyms object using a real API."""
    return Synonyms(actual_api_call, "companies")


@pytest.fixture(scope="function", name="fake_synonym")
def fake_synonym_fixture(fake_api_call: ApiCall) -> Synonym:
    """Return a Synonym object with test values."""
    return Synonym(fake_api_call, "companies", "company_synonym")


@pytest_asyncio.fixture(loop_scope="function", name="create_synonym_async")
async def create_synonym_fixture_async(create_collection_async: None) -> None:
    """Create a synonym in the Typesense server asynchronously."""
    url = "http://localhost:8108/collections/companies/synonyms/company_synonym"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    synonym_data = {
        "synonyms": ["companies", "corporations", "firms"],
    }

    async with httpx.AsyncClient() as client:
        create_synonym_response = await client.put(
            url,
            headers=headers,
            json=synonym_data,
            timeout=3,
        )
        create_synonym_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="fake_synonyms_async")
async def fake_synonyms_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncSynonyms:
    """Return an AsyncSynonyms object with test values."""
    return AsyncSynonyms(fake_api_call_async, "companies")


@pytest_asyncio.fixture(loop_scope="function", name="actual_synonyms_async")
async def actual_synonyms_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncSynonyms:
    """Return an AsyncSynonyms object using a real API."""
    return AsyncSynonyms(actual_api_call_async, "companies")


@pytest_asyncio.fixture(loop_scope="function", name="fake_synonym_async")
async def fake_synonym_fixture_async(fake_api_call_async: AsyncApiCall) -> AsyncSynonym:
    """Return an AsyncSynonym object with test values."""
    return AsyncSynonym(fake_api_call_async, "companies", "company_synonym")
