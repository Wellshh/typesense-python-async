"""Tests for the Synonym class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.collections import Collections
from typesense.async_client.synonym import Synonym, SynonymDeleteSchema
from typesense.async_client.synonyms import SynonymSchema


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Synonym object is initialized correctly."""
    synonym = Synonym(fake_api_call_async, "companies", "company_synonym")

    assert synonym.collection_name == "companies"
    assert synonym.synonym_id == "company_synonym"
    assert_match_object(synonym.api_call, fake_api_call_async)
    assert_object_lists_match(
        synonym.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        synonym.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert synonym._endpoint_path() == "/collections/companies/synonyms/company_synonym"


@pytest.mark.asyncio
async def test_retrieve(fake_synonym_async: Synonym, httpx_mock) -> None:
    """Test that the Synonym object can retrieve an synonym."""
    json_response: SynonymSchema = {
        "id": "company_synonym",
        "synonyms": ["companies", "corporations", "firms"],
    }

    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/synonyms/company_synonym",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_synonym_async.retrieve()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "GET"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/collections/companies/synonyms/company_synonym"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_delete(fake_synonym_async: Synonym, httpx_mock) -> None:
    """Test that the Synonym object can delete an synonym."""
    json_response: SynonymDeleteSchema = {
        "id": "company_synonym",
    }
    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/synonyms/company_synonym",
        method="DELETE",
        json=json_response,
        status_code=200,
    )

    response = await fake_synonym_async.delete()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "DELETE"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/collections/companies/synonyms/company_synonym"
    )
    assert response == {"id": "company_synonym"}


@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_collections_async: Collections,
    delete_all_async: None,
    create_synonym_async: None,
) -> None:
    """Test that the Synonym object can retrieve an synonym from Typesense Server."""
    response = (
        await actual_collections_async["companies"]
        .synonyms["company_synonym"]
        .retrieve()
    )

    assert response["id"] == "company_synonym"

    assert response["synonyms"] == ["companies", "corporations", "firms"]
    assert_to_contain_object(
        response,
        {
            "id": "company_synonym",
            "synonyms": ["companies", "corporations", "firms"],
        },
    )


@pytest.mark.asyncio
async def test_actual_delete(
    actual_collections_async: Collections,
    delete_all_async: None,
    create_synonym_async: None,
) -> None:
    """Test that the Synonym object can delete an synonym from Typesense Server."""
    response = (
        await actual_collections_async["companies"].synonyms["company_synonym"].delete()
    )

    assert response == {"id": "company_synonym"}
