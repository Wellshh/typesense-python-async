"""Tests for the Synonyms class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.collections import Collections
from typesense.async_client.synonyms import (
    Synonyms,
    SynonymSchema,
    SynonymsRetrieveSchema,
)


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Synonyms object is initialized correctly."""
    synonyms = Synonyms(fake_api_call_async, "companies")

    assert_match_object(synonyms.api_call, fake_api_call_async)
    assert_object_lists_match(
        synonyms.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        synonyms.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )

    assert not synonyms.synonyms


def test_get_missing_synonym(fake_synonyms_async: Synonyms) -> None:
    """Test that the Synonyms object can get a missing synonym."""
    synonym = fake_synonyms_async["company_synonym"]

    assert synonym.synonym_id == "company_synonym"
    assert_match_object(synonym.api_call, fake_synonyms_async.api_call)
    assert_object_lists_match(
        synonym.api_call.node_manager.nodes,
        fake_synonyms_async.api_call.node_manager.nodes,
    )
    assert_match_object(
        synonym.api_call.config.nearest_node,
        fake_synonyms_async.api_call.config.nearest_node,
    )
    assert synonym.collection_name == "companies"
    assert synonym._endpoint_path() == "/collections/companies/synonyms/company_synonym"


def test_get_existing_synonym(fake_synonyms_async: Synonyms) -> None:
    """Test that the Synonyms object can get an existing synonym."""
    synonym = fake_synonyms_async["companies"]
    fetched_synonym = fake_synonyms_async["companies"]

    assert len(fake_synonyms_async.synonyms) == 1

    assert synonym is fetched_synonym


@pytest.mark.asyncio
async def test_retrieve(fake_synonyms_async: Synonyms, httpx_mock) -> None:
    """Test that the Synonyms object can retrieve synonyms."""
    json_response: SynonymsRetrieveSchema = {
        "synonyms": [
            {
                "id": "company_synonym",
                "synonyms": ["companies", "corporations", "firms"],
            },
        ],
    }

    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/synonyms/",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_synonyms_async.retrieve()

    assert len(response) == 1
    assert response["synonyms"][0] == {
        "id": "company_synonym",
        "synonyms": ["companies", "corporations", "firms"],
    }
    assert response == json_response


@pytest.mark.asyncio
async def test_create(fake_synonyms_async: Synonyms, httpx_mock) -> None:
    """Test that the Synonyms object can create a synonym."""
    json_response: SynonymSchema = {
        "id": "company_synonym",
        "synonyms": ["companies", "corporations", "firms"],
    }

    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/synonyms/company_synonym",
        method="PUT",
        json=json_response,
        status_code=201,
    )

    await fake_synonyms_async.upsert(
        "company_synonym",
        {"synonyms": ["companies", "corporations", "firms"]},
    )

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "PUT"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/collections/companies/synonyms/company_synonym"
    )
    assert (
        httpx_mock.get_requests()[0].read().decode()
        == '{"synonyms": ["companies", "corporations", "firms"]}'
    )


@pytest.mark.asyncio
async def test_actual_create(
    actual_synonyms_async: Synonyms,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Synonyms object can create an synonym on Typesense Server."""
    response = await actual_synonyms_async.upsert(
        "company_synonym",
        {"synonyms": ["companies", "corporations", "firms"]},
    )

    assert response == {
        "id": "company_synonym",
        "synonyms": ["companies", "corporations", "firms"],
    }


@pytest.mark.asyncio
async def test_actual_update(
    actual_synonyms_async: Synonyms,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Synonyms object can update an synonym on Typesense Server."""
    create_response = await actual_synonyms_async.upsert(
        "company_synonym",
        {"synonyms": ["companies", "corporations", "firms"]},
    )

    assert create_response == {
        "id": "company_synonym",
        "synonyms": ["companies", "corporations", "firms"],
    }

    update_response = await actual_synonyms_async.upsert(
        "company_synonym",
        {"synonyms": ["companies", "corporations"]},
    )

    assert update_response == {
        "id": "company_synonym",
        "synonyms": ["companies", "corporations"],
    }


@pytest.mark.asyncio
async def test_actual_retrieve(
    delete_all_async: None,
    create_synonym_async: None,
    actual_collections_async: Collections,
) -> None:
    """Test that the Synonyms object can retrieve an synonym from Typesense Server."""
    response = await actual_collections_async["companies"].synonyms.retrieve()

    assert len(response["synonyms"]) == 1
    assert_to_contain_object(
        response["synonyms"][0],
        {
            "id": "company_synonym",
            "synonyms": ["companies", "corporations", "firms"],
        },
    )
