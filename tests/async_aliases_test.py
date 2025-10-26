"""Tests for the async Aliases class."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.aliases import Aliases
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.types.alias import AliasesResponseSchema, AliasSchema


@pytest.mark.asyncio
async def test_init_async(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the async Aliases object is initialized correctly."""
    aliases = Aliases(fake_api_call_async)

    assert_match_object(aliases.api_call, fake_api_call_async)
    assert_object_lists_match(
        aliases.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        aliases.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )

    assert not aliases.aliases


@pytest.mark.asyncio
async def test_get_missing_alias_async(fake_aliases_async: Aliases) -> None:
    """Test that the async Aliases object can get a missing alias."""
    alias = fake_aliases_async["company_alias"]

    assert alias.name == "company_alias"
    assert_match_object(alias.api_call, fake_aliases_async.api_call)
    assert_object_lists_match(
        alias.api_call.node_manager.nodes,
        fake_aliases_async.api_call.node_manager.nodes,
    )
    assert_match_object(
        alias.api_call.config.nearest_node,
        fake_aliases_async.api_call.config.nearest_node,
    )
    assert alias._endpoint_path == "/aliases/company_alias"


@pytest.mark.asyncio
async def test_get_existing_alias_async(fake_aliases_async: Aliases) -> None:
    """Test that the async Aliases object can get an existing alias."""
    alias = fake_aliases_async["companies"]
    fetched_alias = fake_aliases_async["companies"]

    assert len(fake_aliases_async.aliases) == 1

    assert alias is fetched_alias


@pytest.mark.asyncio
async def test_retrieve_async(
    fake_aliases_async: Aliases, httpx_mock: HTTPXMock
) -> None:
    """Test that the async Aliases object can retrieve aliases."""
    json_response: AliasesResponseSchema = {
        "aliases": [
            {
                "collection_name": "companies",
                "name": "company_alias",
            },
        ],
    }

    httpx_mock.add_response(
        method="GET",
        url="http://nearest:8108/aliases",
        json=json_response,
    )

    response = await fake_aliases_async.retrieve()

    assert len(response) == 1
    assert response["aliases"][0] == {
        "collection_name": "companies",
        "name": "company_alias",
    }
    assert response == json_response


@pytest.mark.asyncio
async def test_create_async(fake_aliases_async: Aliases, httpx_mock: HTTPXMock) -> None:
    """Test that the async Aliases object can create an alias."""
    json_response: AliasSchema = {
        "collection_name": "companies",
        "name": "company_alias",
    }

    httpx_mock.add_response(
        method="PUT",
        url="http://nearest:8108/aliases/company_alias",
        json=json_response,
    )

    await fake_aliases_async.upsert(
        "company_alias",
        {"collection_name": "companies", "name": "company_alias"},
    )


@pytest.mark.asyncio
async def test_actual_create_async(
    actual_aliases_async: Aliases, delete_all_aliases_async: None
) -> None:
    """Test that the async Aliases object can create an alias on Typesense Server."""
    response = await actual_aliases_async.upsert(
        "company_alias", {"collection_name": "companies"}
    )

    assert response == {"collection_name": "companies", "name": "company_alias"}


@pytest.mark.asyncio
async def test_actual_update_async(
    actual_aliases_async: Aliases,
    delete_all_aliases_async: None,
    delete_all_async: None,
    create_collection_async: None,
    create_another_collection_async: None,
) -> None:
    """Test that the async Aliases object can update an alias on Typesense Server."""
    create_response = await actual_aliases_async.upsert(
        "company_alias",
        {"collection_name": "companies"},
    )

    assert create_response == {"collection_name": "companies", "name": "company_alias"}

    update_response = await actual_aliases_async.upsert(
        "company_alias",
        {"collection_name": "companies_2"},
    )

    assert update_response == {
        "collection_name": "companies_2",
        "name": "company_alias",
    }


@pytest.mark.asyncio
async def test_actual_retrieve_async(
    delete_all_async: None,
    delete_all_aliases_async: None,
    create_alias_async: None,
    actual_aliases_async: Aliases,
) -> None:
    """Test that the async Aliases object can retrieve an alias from Typesense Server."""
    response = await actual_aliases_async.retrieve()

    assert len(response["aliases"]) == 1
    assert_to_contain_object(
        response["aliases"][0],
        {
            "collection_name": "companies",
            "name": "company_alias",
        },
    )
