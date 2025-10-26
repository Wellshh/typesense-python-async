"""Fixtures for the Overrides tests."""

import httpx
import pytest
import pytest_asyncio
import requests

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.override import Override as AsyncOverride
from typesense.async_client.overrides import Overrides as AsyncOverrides
from typesense.override import Override
from typesense.overrides import Overrides


@pytest.fixture(scope="function", name="create_override")
def create_override_fixture(create_collection: None) -> None:
    """Create an override in the Typesense server."""
    url = "http://localhost:8108/collections/companies/overrides/company_override"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    override_data = {
        "rule": {"match": "exact", "query": "companies"},
        "filter_by": "num_employees>10",
    }

    response = requests.put(url, headers=headers, json=override_data, timeout=3)
    response.raise_for_status()


@pytest.fixture(scope="function", name="actual_overrides")
def actual_overrides_fixture(actual_api_call: ApiCall) -> Overrides:
    """Return a Overrides object using a real API."""
    return Overrides(actual_api_call, "companies")


@pytest.fixture(scope="function", name="fake_overrides")
def fake_overrides_fixture(fake_api_call: ApiCall) -> Overrides:
    """Return a Override object with test values."""
    return Overrides(fake_api_call, "companies")


@pytest.fixture(scope="function", name="fake_override")
def fake_override_fixture(fake_api_call: ApiCall) -> Override:
    """Return a Override object with test values."""
    return Override(fake_api_call, "companies", "company_override")


@pytest_asyncio.fixture(loop_scope="function", name="create_override_async")
async def create_override_fixture_async(create_collection_async: None) -> None:
    """Create an override in the Typesense server asynchronously."""
    url = "http://localhost:8108/collections/companies/overrides/company_override"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    override_data = {
        "rule": {"match": "exact", "query": "companies"},
        "filter_by": "num_employees>10",
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=override_data, timeout=3)
        response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="actual_overrides_async")
async def actual_overrides_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncOverrides:
    """Return an AsyncOverrides object using a real API."""
    return AsyncOverrides(actual_api_call_async, "companies")


@pytest_asyncio.fixture(loop_scope="function", name="fake_overrides_async")
async def fake_overrides_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncOverrides:
    """Return an AsyncOverrides object with test values."""
    return AsyncOverrides(fake_api_call_async, "companies")


@pytest_asyncio.fixture(loop_scope="function", name="fake_override_async")
async def fake_override_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncOverride:
    """Return an AsyncOverride object with test values."""
    return AsyncOverride(fake_api_call_async, "companies", "company_override")
