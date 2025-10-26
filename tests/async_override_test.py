"""Tests for the Override class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.collections import Collections
from typesense.async_client.override import Override, OverrideDeleteSchema
from typesense.types.override import OverrideSchema


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Override object is initialized correctly."""
    override = Override(fake_api_call_async, "companies", "company_override")

    assert override.collection_name == "companies"
    assert override.override_id == "company_override"
    assert_match_object(override.api_call, fake_api_call_async)
    assert_object_lists_match(
        override.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        override.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert (
        override._endpoint_path() == "/collections/companies/overrides/company_override"
    )


@pytest.mark.asyncio
async def test_retrieve(fake_override_async: Override, httpx_mock) -> None:
    """Test that the Override object can retrieve an override."""
    json_response: OverrideSchema = {
        "rule": {
            "match": "contains",
            "query": "companies",
        },
        "filter_by": "num_employees>10",
    }

    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/overrides/company_override",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_override_async.retrieve()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "GET"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/collections/companies/overrides/company_override"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_delete(fake_override_async: Override, httpx_mock) -> None:
    """Test that the Override object can delete an override."""
    json_response: OverrideDeleteSchema = {
        "id": "company_override",
    }
    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/overrides/company_override",
        method="DELETE",
        json=json_response,
        status_code=200,
    )

    response = await fake_override_async.delete()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "DELETE"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/collections/companies/overrides/company_override"
    )
    assert response == {"id": "company_override"}


@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_collections_async: Collections,
    delete_all_async: None,
    create_override_async: None,
) -> None:
    """Test that the Override object can retrieve an override from Typesense Server."""
    response = (
        await actual_collections_async["companies"]
        .overrides["company_override"]
        .retrieve()
    )

    assert response["rule"] == {
        "match": "exact",
        "query": "companies",
    }
    assert response["filter_by"] == "num_employees>10"
    assert_to_contain_object(
        response,
        {
            "rule": {
                "match": "exact",
                "query": "companies",
            },
            "filter_by": "num_employees>10",
        },
    )


@pytest.mark.asyncio
async def test_actual_delete(
    actual_collections_async: Collections,
    delete_all_async: None,
    create_override_async: None,
) -> None:
    """Test that the Override object can delete an override from Typesense Server."""
    response = (
        await actual_collections_async["companies"]
        .overrides["company_override"]
        .delete()
    )

    assert response == {"id": "company_override"}
