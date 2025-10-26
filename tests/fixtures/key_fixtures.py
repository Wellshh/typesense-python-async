"""Fixtures for the key tests."""

import httpx
import pytest
import pytest_asyncio
import requests

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.key import Key as AsyncKey
from typesense.async_client.keys import Keys as AsyncKeys
from typesense.key import Key
from typesense.keys import Keys


@pytest.fixture(scope="function", name="delete_all_keys")
def clear_typesense_keys() -> None:
    """Remove all keys from the Typesense server."""
    url = "http://localhost:8108/keys"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    # Get the list of keys
    response = requests.get(url, headers=headers, timeout=3)
    response.raise_for_status()

    keys = response.json()

    # Delete each key
    for key in keys["keys"]:
        key_name = key.get("id")
        delete_url = f"{url}/{key_name}"
        delete_response = requests.delete(delete_url, headers=headers, timeout=3)
        delete_response.raise_for_status()


@pytest.fixture(scope="function", name="create_key_id")
def create_key_fixture() -> int:
    """Create a key set in the Typesense server."""
    url = "http://localhost:8108/keys"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    api_key_data = {
        "actions": ["documents:search"],
        "collections": ["companies"],
        "description": "Search-only key",
    }

    response = requests.post(url, headers=headers, json=api_key_data, timeout=3)
    response.raise_for_status()
    key_id: int = response.json()["id"]
    return key_id


@pytest.fixture(scope="function", name="actual_keys")
def actual_keys_fixture(actual_api_call: ApiCall) -> Keys:
    """Return a Keys object using a real API."""
    return Keys(actual_api_call)


@pytest.fixture(scope="function", name="fake_keys")
def fake_keys_fixture(fake_api_call: ApiCall) -> Keys:
    """Return a AnalyticsRule object with test values."""
    return Keys(fake_api_call)


@pytest.fixture(scope="function", name="fake_key")
def fake_key_fixture(fake_api_call: ApiCall) -> Key:
    """Return a Key object with test values."""
    return Key(fake_api_call, 1)


@pytest_asyncio.fixture(loop_scope="function", name="delete_all_keys_async")
async def clear_typesense_keys_async() -> None:
    """Remove all keys from the Typesense server asynchronously."""
    url = "http://localhost:8108/keys"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        keys = response.json()

        for key in keys["keys"]:
            key_name = key.get("id")
            delete_url = f"{url}/{key_name}"
            delete_response = await client.delete(
                delete_url, headers=headers, timeout=3
            )
            delete_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="create_key_id_async")
async def create_key_fixture_async() -> int:
    """Create a key set in the Typesense server asynchronously."""
    url = "http://localhost:8108/keys"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    api_key_data = {
        "actions": ["documents:search"],
        "collections": ["companies"],
        "description": "Search-only key",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=api_key_data, timeout=3)
        response.raise_for_status()
        key_id: int = response.json()["id"]
        return key_id


@pytest_asyncio.fixture(loop_scope="function", name="actual_keys_async")
async def actual_keys_fixture_async(actual_api_call_async: AsyncApiCall) -> AsyncKeys:
    """Return an AsyncKeys object using a real API."""
    return AsyncKeys(actual_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_keys_async")
async def fake_keys_fixture_async(fake_api_call_async: AsyncApiCall) -> AsyncKeys:
    """Return an AsyncKeys object with test values."""
    return AsyncKeys(fake_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_key_async")
async def fake_key_fixture_async(fake_api_call_async: AsyncApiCall) -> AsyncKey:
    """Return an AsyncKey object with test values."""
    return AsyncKey(fake_api_call_async, 1)
