"""Tests for the Overrides class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.collections import Collections
from typesense.async_client.overrides import (
    OverrideRetrieveSchema,
    Overrides,
    OverrideSchema,
)


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Overrides object is initialized correctly."""
    overrides = Overrides(fake_api_call_async, "companies")

    assert_match_object(overrides.api_call, fake_api_call_async)
    assert_object_lists_match(
        overrides.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        overrides.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )

    assert not overrides.overrides


def test_get_missing_override(fake_overrides_async: Overrides) -> None:
    """Test that the Overrides object can get a missing override."""
    override = fake_overrides_async["company_override"]

    assert override.override_id == "company_override"
    assert_match_object(override.api_call, fake_overrides_async.api_call)
    assert_object_lists_match(
        override.api_call.node_manager.nodes,
        fake_overrides_async.api_call.node_manager.nodes,
    )
    assert_match_object(
        override.api_call.config.nearest_node,
        fake_overrides_async.api_call.config.nearest_node,
    )
    assert override.collection_name == "companies"
    assert (
        override._endpoint_path() == "/collections/companies/overrides/company_override"
    )


def test_get_existing_override(fake_overrides_async: Overrides) -> None:
    """Test that the Overrides object can get an existing override."""
    override = fake_overrides_async["companies"]
    fetched_override = fake_overrides_async["companies"]

    assert len(fake_overrides_async.overrides) == 1

    assert override is fetched_override


@pytest.mark.asyncio
async def test_retrieve(fake_overrides_async: Overrides, httpx_mock) -> None:
    """Test that the Overrides object can retrieve overrides."""
    json_response: OverrideRetrieveSchema = {
        "overrides": [
            {
                "id": "company_override",
                "rule": {"match": "exact", "query": "companies"},
            },
        ],
    }
    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/overrides/",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_overrides_async.retrieve()

    assert len(response) == 1
    assert response["overrides"][0] == {
        "id": "company_override",
        "rule": {"match": "exact", "query": "companies"},
    }
    assert response == json_response


@pytest.mark.asyncio
async def test_create(fake_overrides_async: Overrides, httpx_mock) -> None:
    """Test that the Overrides object can create a override."""
    json_response: OverrideSchema = {
        "id": "company_override",
        "rule": {"match": "exact", "query": "companies"},
    }

    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/overrides/company_override",
        method="PUT",
        json=json_response,
        status_code=201,
    )

    await fake_overrides_async.upsert(
        "company_override",
        {"rule": {"match": "exact", "query": "companies"}},
    )

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "PUT"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/collections/companies/overrides/company_override"
    )
    assert (
        httpx_mock.get_requests()[0].read().decode()
        == '{"rule": {"match": "exact", "query": "companies"}}'
    )


@pytest.mark.asyncio
async def test_actual_create(
    actual_overrides_async: Overrides,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Overrides object can create an override on Typesense Server."""
    response = await actual_overrides_async.upsert(
        "company_override",
        {
            "rule": {"match": "exact", "query": "companies"},
            "filter_by": "num_employees>10",
        },
    )

    assert response == {
        "id": "company_override",
        "rule": {"match": "exact", "query": "companies"},
        "filter_by": "num_employees>10",
    }


@pytest.mark.asyncio
async def test_actual_update(
    actual_overrides_async: Overrides,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Overrides object can update an override on Typesense Server."""
    create_response = await actual_overrides_async.upsert(
        "company_override",
        {
            "rule": {"match": "exact", "query": "companies"},
            "filter_by": "num_employees>10",
        },
    )

    assert create_response == {
        "id": "company_override",
        "rule": {"match": "exact", "query": "companies"},
        "filter_by": "num_employees>10",
    }

    update_response = await actual_overrides_async.upsert(
        "company_override",
        {
            "rule": {"match": "contains", "query": "companies"},
            "filter_by": "num_employees>20",
        },
    )

    assert update_response == {
        "id": "company_override",
        "rule": {"match": "contains", "query": "companies"},
        "filter_by": "num_employees>20",
    }


@pytest.mark.asyncio
async def test_actual_retrieve(
    delete_all_async: None,
    create_override_async: None,
    actual_collections_async: Collections,
) -> None:
    """Test that the Overrides object can retrieve an override from Typesense Server."""
    response = await actual_collections_async["companies"].overrides.retrieve()

    assert len(response["overrides"]) == 1
    assert_to_contain_object(
        response["overrides"][0],
        {
            "id": "company_override",
            "rule": {"match": "exact", "query": "companies"},
            "filter_by": "num_employees>10",
        },
    )
