"""Tests for the async Alias class."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.alias import Alias
from typesense.async_client.aliases import Aliases
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.types.alias import AliasSchema


@pytest.mark.asyncio
async def test_init_async(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the async Alias object is initialized correctly."""
    alias = Alias(fake_api_call_async, "company_alias")

    assert alias.name == "company_alias"
    assert_match_object(alias.api_call, fake_api_call_async)
    assert_object_lists_match(
        alias.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        alias.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert alias._endpoint_path == "/aliases/company_alias"


@pytest.mark.asyncio
async def test_retrieve_async(fake_alias_async: Alias, httpx_mock: HTTPXMock) -> None:
    """Test that the async Alias object can retrieve an alias."""
    json_response: AliasSchema = {
        "collection_name": "companies",
        "name": "company_alias",
    }

    httpx_mock.add_response(
        method="GET",
        url="http://nearest:8108/aliases/company_alias",
        json=json_response,
    )

    response = await fake_alias_async.retrieve()

    assert response == json_response


@pytest.mark.asyncio
async def test_delete_async(fake_alias_async: Alias, httpx_mock: HTTPXMock) -> None:
    """Test that the async Alias object can delete an alias."""
    json_response: AliasSchema = {
        "collection_name": "companies",
        "name": "company_alias",
    }

    httpx_mock.add_response(
        method="DELETE",
        url="http://nearest:8108/aliases/company_alias",
        json=json_response,
    )

    response = await fake_alias_async.delete()

    assert response == json_response


@pytest.mark.asyncio
async def test_actual_retrieve_async(
    actual_aliases_async: Aliases,
    delete_all_aliases_async: None,
    delete_all_async: None,
    create_alias_async: None,
) -> None:
    """Test that the async Alias object can retrieve an alias from Typesense Server."""
    response = await actual_aliases_async["company_alias"].retrieve()

    assert response["collection_name"] == "companies"
    assert response["name"] == "company_alias"

    assert_to_contain_object(
        response,
        {
            "collection_name": "companies",
            "name": "company_alias",
        },
    )


@pytest.mark.asyncio
async def test_actual_delete_async(
    actual_aliases_async: Aliases,
    delete_all_aliases_async: None,
    delete_all_async: None,
    create_alias_async: None,
) -> None:
    """Test that the async Alias object can delete an alias from Typesense Server."""
    response = await actual_aliases_async["company_alias"].delete()

    assert response == {
        "collection_name": "companies",
        "name": "company_alias",
    }
