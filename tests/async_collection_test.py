"""Tests for the async Collection class."""

from __future__ import annotations

import time

import pytest
from pytest_httpx import HTTPXMock

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.collection import Collection
from typesense.async_client.collections import Collections
from typesense.types.collection import CollectionSchema


@pytest.mark.asyncio
async def test_init_async(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the async Collection object is initialized correctly."""
    collection = Collection(fake_api_call_async, "companies")

    assert collection.name == "companies"
    assert_match_object(collection.api_call, fake_api_call_async)
    assert_object_lists_match(
        collection.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        collection.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert collection.overrides.collection_name == "companies"
    assert collection._endpoint_path == "/collections/companies"


@pytest.mark.asyncio
async def test_retrieve_async(
    fake_collection_async: Collection, httpx_mock: HTTPXMock
) -> None:
    """Test that the async Collection object can retrieve a collection."""
    time_now = int(time.time())

    json_response: CollectionSchema = {
        "created_at": time_now,
        "default_sorting_field": "num_employees",
        "enable_nested_fields": False,
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
        "name": "companies",
        "num_documents": 0,
        "symbols_to_index": [],
        "token_separators": [],
    }

    httpx_mock.add_response(
        method="GET",
        url="http://nearest:8108/collections/companies",
        json=json_response,
    )

    response = await fake_collection_async.retrieve()

    assert response == json_response


@pytest.mark.asyncio
async def test_update_async(
    fake_collection_async: Collection, httpx_mock: HTTPXMock
) -> None:
    """Test that the async Collection object can update a collection."""
    json_response: CollectionSchema = {
        "created_at": 1619711487,
        "default_sorting_field": "num_employees",
        "enable_nested_fields": False,
        "fields": [
            {
                "name": "company_name",
                "type": "string",
            },
            {
                "name": "num_employees",
                "type": "int32",
            },
            {
                "name": "num_locations",
                "type": "int32",
            },
        ],
        "name": "companies",
        "num_documents": 0,
        "symbols_to_index": [],
        "token_separators": [],
    }

    httpx_mock.add_response(
        method="PATCH",
        url="http://nearest:8108/collections/companies",
        json=json_response,
    )

    response = await fake_collection_async.update(
        schema_change={
            "fields": [
                {
                    "name": "num_locations",
                    "type": "int32",
                },
            ],
        },
    )

    assert response == json_response


@pytest.mark.asyncio
async def test_delete_async(
    fake_collection_async: Collection, httpx_mock: HTTPXMock
) -> None:
    """Test that the async Collection object can delete a collection."""
    json_response: CollectionSchema = {
        "created_at": 1619711487,
        "default_sorting_field": "num_employees",
        "enable_nested_fields": False,
        "fields": [
            {
                "name": "company_name",
                "type": "string",
            },
            {
                "name": "num_employees",
                "type": "int32",
            },
            {
                "name": "num_locations",
                "type": "int32",
            },
        ],
        "name": "companies",
        "num_documents": 0,
        "symbols_to_index": [],
        "token_separators": [],
    }

    httpx_mock.add_response(
        method="DELETE",
        url="http://nearest:8108/collections/companies",
        json=json_response,
    )

    response = await fake_collection_async.delete()

    assert response == json_response


@pytest.mark.asyncio
async def test_actual_retrieve_async(
    actual_collections_async: Collections,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the async Collection object can retrieve a collection."""
    response = await actual_collections_async["companies"].retrieve()

    expected: CollectionSchema = {
        "default_sorting_field": "num_employees",
        "enable_nested_fields": False,
        "fields": [
            {
                "name": "company_name",
                "type": "string",
                "facet": False,
                "index": True,
                "optional": False,
                "locale": "",
                "sort": False,
                "infix": False,
                "stem": False,
                "stem_dictionary": "",
                "store": True,
            },
            {
                "name": "num_employees",
                "type": "int32",
                "facet": False,
                "index": True,
                "optional": False,
                "locale": "",
                "sort": True,
                "infix": False,
                "stem": False,
                "stem_dictionary": "",
                "store": True,
            },
        ],
        "name": "companies",
        "num_documents": 0,
        "symbols_to_index": [],
        "token_separators": [],
    }

    response.pop("created_at")

    assert response == expected


@pytest.mark.asyncio
async def test_actual_update_async(
    actual_collections_async: Collections,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the async Collection object can update a collection."""
    response = await actual_collections_async["companies"].update(
        {"fields": [{"name": "num_locations", "type": "int32"}]},
    )

    expected: CollectionSchema = {
        "fields": [
            {
                "name": "num_locations",
                "type": "int32",
            },
        ],
    }

    assert_to_contain_object(response.get("fields")[0], expected.get("fields")[0])
