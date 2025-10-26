"""Fixtures for Collections tests."""

import httpx
import pytest
import pytest_asyncio
import requests

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.collection import Collection as AsyncCollection
from typesense.async_client.collections import Collections as AsyncCollections
from typesense.collection import Collection
from typesense.collections import Collections


@pytest.fixture(scope="function", name="delete_all")
def clear_typesense_collections() -> None:
    """Remove all collections from the Typesense server."""
    url = "http://localhost:8108/collections"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    # Get the list of collections
    response = requests.get(url, headers=headers, timeout=3)
    response.raise_for_status()
    collections = response.json()

    # Delete each collection
    for collection in collections:
        collection_name = collection["name"]
        delete_url = f"{url}/{collection_name}"
        delete_response = requests.delete(delete_url, headers=headers, timeout=3)
        delete_response.raise_for_status()


@pytest.fixture(scope="function", name="create_collection")
def create_collection_fixture() -> None:
    """Create a collection in the Typesense server."""
    url = "http://localhost:8108/collections"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    collection_data = {
        "name": "companies",
        "fields": [
            {
                "name": "company_name",
                "type": "string",
            },
            {
                "name": "num_employees",
                "type": "int32",
            },
        ],
        "default_sorting_field": "num_employees",
    }

    response = requests.post(url, headers=headers, json=collection_data, timeout=3)
    response.raise_for_status()


@pytest.fixture(scope="function", name="create_another_collection")
def create_another_collection_fixture() -> None:
    """Create a collection in the Typesense server."""
    url = "http://localhost:8108/collections"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    collection_data = {
        "name": "companies_2",
        "fields": [
            {
                "name": "company_name",
                "type": "string",
            },
            {
                "name": "num_employees",
                "type": "int32",
            },
        ],
        "default_sorting_field": "num_employees",
    }

    response = requests.post(url, headers=headers, json=collection_data, timeout=3)
    response.raise_for_status()


@pytest.fixture(scope="function", name="actual_collections")
def actual_collections_fixture(actual_api_call: ApiCall) -> Collections:
    """Return a Collections object using a real API."""
    return Collections(actual_api_call)


@pytest.fixture(scope="function", name="fake_collections")
def fake_collections_fixture(fake_api_call: ApiCall) -> Collections:
    """Return a Collections object with test values."""
    return Collections(fake_api_call)


@pytest.fixture(scope="function", name="fake_collection")
def fake_collection_fixture(fake_api_call: ApiCall) -> Collection:
    """Return a Collection object with test values."""
    return Collection(fake_api_call, "companies")


@pytest_asyncio.fixture(loop_scope="function", name="delete_all_async")
async def clear_typesense_collections_async() -> None:
    """Remove all collections from the Typesense server asynchronously."""
    url = "http://localhost:8108/collections"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        collections = response.json()

        for collection in collections:
            collection_name = collection["name"]
            delete_url = f"{url}/{collection_name}"
            delete_response = await client.delete(
                delete_url, headers=headers, timeout=3
            )
            delete_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="create_collection_async")
async def create_collection_fixture_async() -> None:
    """Create a collection in the Typesense server asynchronously."""
    url = "http://localhost:8108/collections"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    collection_data = {
        "name": "companies",
        "fields": [
            {
                "name": "company_name",
                "type": "string",
            },
            {
                "name": "num_employees",
                "type": "int32",
            },
        ],
        "default_sorting_field": "num_employees",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers=headers, json=collection_data, timeout=3
        )
        response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="actual_collections_async")
async def actual_collections_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncCollections:
    """Return an AsyncCollections object using a real API."""
    return AsyncCollections(actual_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_collections_async")
async def fake_collections_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncCollections:
    """Return an AsyncCollections object with test values."""
    return AsyncCollections(fake_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_collection_async")
async def fake_collection_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncCollection:
    """Return an AsyncCollection object with test values."""
    return AsyncCollection(fake_api_call_async, "companies")


@pytest_asyncio.fixture(loop_scope="function", name="create_another_collection_async")
async def create_another_collection_fixture_async() -> None:
    """Create another collection in the Typesense server asynchronously."""
    url = "http://localhost:8108/collections"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    collection_data = {
        "name": "companies_2",
        "fields": [
            {
                "name": "company_name",
                "type": "string",
            },
            {
                "name": "num_employees",
                "type": "int32",
            },
        ],
        "default_sorting_field": "num_employees",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers=headers, json=collection_data, timeout=3
        )
        response.raise_for_status()
