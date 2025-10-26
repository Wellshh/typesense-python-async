"""Fixtures for alias tests."""

import httpx
import pytest
import requests
import pytest_asyncio

from typesense.alias import Alias
from typesense.aliases import Aliases
from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall


@pytest.fixture(scope="function", name="delete_all_aliases")
def clear_typesense_aliases() -> None:
    """Remove all aliases from the Typesense server."""
    url = "http://localhost:8108/aliases"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    # Get the list of collections
    response = requests.get(url, headers=headers, timeout=3)
    response.raise_for_status()

    aliases = response.json()

    # Delete each alias
    for alias in aliases["aliases"]:
        alias_name = alias.get("name")
        delete_url = f"{url}/{alias_name}"
        delete_response = requests.delete(delete_url, headers=headers, timeout=3)
        delete_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="delete_all_aliases_async")
async def clear_typesense_aliases_async() -> None:
    """Remove all aliases from the Typesense server asynchronously."""
    url = "http://localhost:8108/aliases"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    # Get the list of aliases
    response = await httpx.AsyncClient().get(url, headers=headers, timeout=3)
    response.raise_for_status()
    aliases = response.json()

    # Delete each alias
    for alias in aliases["aliases"]:
        alias_name = alias.get("name")
        delete_url = f"{url}/{alias_name}"
        delete_response = await httpx.AsyncClient().delete(
            delete_url, headers=headers, timeout=3
        )
        delete_response.raise_for_status()


@pytest.fixture(scope="function", name="create_alias")
def create_alias_fixture(create_collection: None) -> None:
    """Create an alias in the Typesense server."""
    url = "http://localhost:8108/aliases/company_alias"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    alias_data = {
        "collection_name": "companies",
    }

    alias_creation_response = requests.put(
        url,
        headers=headers,
        json=alias_data,
        timeout=3,
    )
    alias_creation_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="create_alias_async")
async def create_alias_fixture_async(create_collection_async: None) -> None:
    """Create an alias in the Typesense server asynchronously."""
    url = "http://localhost:8108/aliases/company_alias"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    alias_data = {
        "collection_name": "companies",
    }
    alias_creation_response = await httpx.AsyncClient().put(
        url, headers=headers, json=alias_data, timeout=3
    )
    alias_creation_response.raise_for_status()


@pytest.fixture(scope="function", name="actual_aliases")
def actual_aliases_fixture(actual_api_call: ApiCall) -> Aliases:
    """Return a Aliases object using a real API."""
    return Aliases(actual_api_call)


@pytest_asyncio.fixture(loop_scope="function", name="actual_aliases_async")
async def actual_aliases_fixture_async(actual_api_call_async: AsyncApiCall) -> Aliases:
    """Return a Aliases object using a real API asynchronously."""
    return Aliases(actual_api_call_async)


@pytest.fixture(scope="function", name="fake_aliases")
def fake_aliases_fixture(fake_api_call: ApiCall) -> Aliases:
    """Return a Aliases object with test values."""
    return Aliases(fake_api_call)


@pytest_asyncio.fixture(loop_scope="function", name="fake_aliases_async")
async def fake_aliases_fixture_async(fake_api_call_async: AsyncApiCall) -> Aliases:
    """Return a Aliases object with test values asynchronously."""
    return Aliases(fake_api_call_async)


@pytest.fixture(scope="function", name="fake_alias")
def fake_alias_fixture(fake_api_call: ApiCall) -> Alias:
    """Return a Alias object with test values."""
    return Alias(fake_api_call, "company_alias")


@pytest_asyncio.fixture(loop_scope="function", name="fake_alias_async")
async def fake_alias_fixture_async(fake_api_call_async: AsyncApiCall) -> Alias:
    """Return a Alias object with test values asynchronously."""
    return Alias(fake_api_call_async, "company_alias")
