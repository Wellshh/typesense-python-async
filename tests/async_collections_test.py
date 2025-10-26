"""Tests for the async Collections class."""

from __future__ import annotations

import sys

import pytest
from pytest_httpx import HTTPXMock

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from tests.utils.object_assertions import assert_match_object, assert_object_lists_match
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.collections import Collections
from typesense.types.collection import CollectionSchema


@pytest.mark.asyncio
async def test_init_async(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the async Collections object is initialized correctly."""
    collections = Collections(fake_api_call_async)

    assert_match_object(collections.api_call, fake_api_call_async)
    assert_object_lists_match(
        collections.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        collections.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert not collections.collections


@pytest.mark.asyncio
async def test_get_missing_collection_async(
    fake_collections_async: Collections,
) -> None:
    """Test that the async Collections object can get a missing collection."""
    collection = fake_collections_async["companies"]

    assert collection.name == "companies"
    assert_match_object(collection.api_call, fake_collections_async.api_call)
    assert_object_lists_match(
        collection.api_call.node_manager.nodes,
        fake_collections_async.api_call.node_manager.nodes,
    )
    assert_match_object(
        collection.api_call.config.nearest_node,
        fake_collections_async.api_call.config.nearest_node,
    )
    assert collection.overrides.collection_name == "companies"
    assert collection._endpoint_path == "/collections/companies"


@pytest.mark.asyncio
async def test_get_existing_collection_async(
    fake_collections_async: Collections,
) -> None:
    """Test that the async Collections object can get an existing collection."""
    collection = fake_collections_async["companies"]
    fetched_collection = fake_collections_async["companies"]

    assert len(fake_collections_async.collections) == 1

    assert collection is fetched_collection


@pytest.mark.asyncio
async def test_retrieve_async(
    fake_collections_async: Collections, httpx_mock: HTTPXMock
) -> None:
    """Test that the async Collections object can retrieve collections."""
    json_response: typing.List[CollectionSchema] = [
        {
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
        },
        {
            "created_at": 1619711488,
            "default_sorting_field": "likes",
            "enable_nested_fields": False,
            "fields": [
                {
                    "name": "name",
                    "type": "string",
                },
                {
                    "name": "likes",
                    "type": "int32",
                },
            ],
            "name": "posts",
            "num_documents": 0,
            "symbols_to_index": [],
            "token_separators": [],
        },
    ]

    httpx_mock.add_response(
        method="GET",
        url="http://nearest:8108/collections",
        json=json_response,
    )

    response = await fake_collections_async.retrieve()

    assert len(response) == 2
    assert response[0]["name"] == "companies"
    assert response[1]["name"] == "posts"
    assert response == json_response


@pytest.mark.asyncio
async def test_create_async(
    fake_collections_async: Collections, httpx_mock: HTTPXMock
) -> None:
    """Test that the async Collections object can create a collection."""
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
        ],
        "name": "companies",
        "num_documents": 0,
        "symbols_to_index": [],
        "token_separators": [],
    }

    httpx_mock.add_response(
        method="POST",
        url="http://nearest:8108/collections",
        json=json_response,
    )

    await fake_collections_async.create(
        {
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
        },
    )


@pytest.mark.asyncio
async def test_actual_create_async(
    actual_collections_async: Collections, delete_all_async: None
) -> None:
    """Test that the async Collections object can create a collection on Typesense Server."""
    expected: CollectionSchema = {
        "default_sorting_field": "",
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
                "sort": False,
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

    response = await actual_collections_async.create(
        {
            "name": "companies",
            "fields": [
                {
                    "name": "company_name",
                    "type": "string",
                },
                {
                    "name": "num_employees",
                    "type": "int32",
                    "sort": False,
                },
            ],
        },
    )

    response.pop("created_at")

    assert response == expected


@pytest.mark.asyncio
async def test_actual_retrieve_async(
    actual_collections_async: Collections,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the async Collections object can retrieve collections."""
    response = await actual_collections_async.retrieve()

    expected: typing.List[CollectionSchema] = [
        {
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
        },
    ]

    response[0].pop("created_at")
    assert response == expected


@pytest.mark.asyncio
async def test_actual_contains_async(
    actual_collections_async: Collections,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the async Collections object can check if a collection exists in Typesense."""
    assert await actual_collections_async.__contains__("companies")
    assert not await actual_collections_async.__contains__("non_existent_collection")
    assert not await actual_collections_async.__contains__("non_existent_collection")
