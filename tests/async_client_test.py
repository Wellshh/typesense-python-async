"""Tests for the AsyncClient class."""

import pytest

from tests.fixtures.document_fixtures import Companies
from tests.utils.object_assertions import assert_match_object, assert_object_lists_match
from typesense.async_client.async_client import AsyncClient
from typesense.configuration import ConfigDict


@pytest.mark.asyncio
async def test_client_init_async(fake_config_dict: ConfigDict) -> None:
    """Test the AsyncClient class __init__ method."""
    fake_client = AsyncClient(fake_config_dict)
    assert fake_client.config == fake_client.api_call.config

    assert_match_object(fake_client.api_call.config, fake_client.config)
    assert_object_lists_match(
        fake_client.api_call.node_manager.nodes, fake_client.config.nodes
    )
    assert_match_object(
        fake_client.api_call.config.nearest_node,
        fake_client.config.nearest_node,
    )

    assert fake_client.collections
    assert fake_client.collections.collections is not None
    assert fake_client.multi_search
    assert fake_client.keys
    assert fake_client.keys.keys is not None
    assert fake_client.aliases
    assert fake_client.aliases.aliases is not None
    assert fake_client.analytics
    assert fake_client.analytics.rules
    assert fake_client.analytics.rules.rules is not None
    assert fake_client.operations
    assert fake_client.debug


@pytest.mark.asyncio
async def test_get_collection_async(fake_client_async: AsyncClient) -> None:
    """Test the AsyncClient class get_collection method."""
    collection = fake_client_async.typed_collection(model=Companies, name="companies")

    assert collection
    assert collection.name == "companies"
    assert collection.documents.documents is not None


@pytest.mark.asyncio
async def test_get_collection_no_name_async(fake_client_async: AsyncClient) -> None:
    """Test the AsyncClient class get_collection method."""
    collection = fake_client_async.typed_collection(model=Companies)

    assert collection
    assert collection.name == "companies"
    assert collection.documents.documents is not None


@pytest.mark.asyncio
async def test_retrieve_collection_actual_async(
    actual_client_async: AsyncClient,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the async client can retrieve an actual collection."""
    collection = actual_client_async.typed_collection(model=Companies, name="companies")

    assert collection is not None


@pytest.mark.asyncio
async def test_retrieve_collection_actual_no_name_async(
    actual_client_async: AsyncClient,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the async client can retrieve an actual collection."""
    collection = actual_client_async.typed_collection(model=Companies)

    assert collection is not None
