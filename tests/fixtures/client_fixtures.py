"""Fixtures for the client tests."""

import pytest
import pytest_asyncio

from typesense.async_client.async_client import AsyncClient
from typesense.client import Client
from typesense.configuration import ConfigDict


@pytest.fixture(scope="function", name="fake_client")
def fake_client_fixture(
    fake_config_dict: ConfigDict,
) -> Client:
    """Return a client object with test values."""
    return Client(fake_config_dict)


@pytest.fixture(scope="function", name="actual_client")
def actual_client_fixture(actual_config_dict: ConfigDict) -> Client:
    """Return a client object using a real API."""
    return Client(actual_config_dict)


@pytest_asyncio.fixture(loop_scope="function", name="fake_client_async")
async def fake_client_fixture_async(
    fake_config_dict: ConfigDict,
) -> AsyncClient:
    """Return an AsyncClient object with test values."""
    return AsyncClient(fake_config_dict)


@pytest_asyncio.fixture(loop_scope="function", name="actual_client_async")
async def actual_client_fixture_async(actual_config_dict: ConfigDict) -> AsyncClient:
    """Return an AsyncClient object using a real API."""
    return AsyncClient(actual_config_dict)
