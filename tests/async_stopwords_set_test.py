"""Tests for the StopwordsSet class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import assert_match_object, assert_object_lists_match
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.stopwords import Stopwords
from typesense.async_client.stopwords_set import StopwordsSet
from typesense.types.stopword import StopwordDeleteSchema, StopwordSchema


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the StopwordsSet object is initialized correctly."""
    stopword_set = StopwordsSet(fake_api_call_async, "company_stopwords")

    assert stopword_set.stopwords_set_id == "company_stopwords"
    assert_match_object(stopword_set.api_call, fake_api_call_async)
    assert_object_lists_match(
        stopword_set.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        stopword_set.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert stopword_set._endpoint_path == "/stopwords/company_stopwords"


@pytest.mark.asyncio
async def test_retrieve(fake_stopwords_set_async: StopwordsSet, httpx_mock) -> None:
    """Test that the StopwordsSet object can retrieve an stopword_set."""
    json_response: StopwordSchema = {
        "id": "company_stopwords",
        "stopwords": ["a", "an", "the"],
    }

    httpx_mock.add_response(
        url="http://nearest:8108/stopwords/company_stopwords",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_stopwords_set_async.retrieve()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "GET"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/stopwords/company_stopwords"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_delete(fake_stopwords_set_async: StopwordsSet, httpx_mock) -> None:
    """Test that the StopwordsSet object can delete an stopword_set."""
    json_response: StopwordDeleteSchema = {
        "id": "company_stopwords",
    }
    httpx_mock.add_response(
        url="http://nearest:8108/stopwords/company_stopwords",
        method="DELETE",
        json=json_response,
        status_code=200,
    )

    response = await fake_stopwords_set_async.delete()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "DELETE"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/stopwords/company_stopwords"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_stopwords_async: Stopwords,
    delete_all_stopwords_async: None,
    delete_all_async: None,
    create_stopword_async: None,
) -> None:
    """Test that the StopwordsSet object can retrieve an stopword_set from Typesense Server."""
    response = await actual_stopwords_async["company_stopwords"].retrieve()

    assert response == {
        "stopwords": {
            "id": "company_stopwords",
            "stopwords": ["and", "is", "the"],
        },
    }


@pytest.mark.asyncio
async def test_actual_delete(
    actual_stopwords_async: Stopwords,
    create_stopword_async: None,
) -> None:
    """Test that the StopwordsSet object can delete an stopword_set from Typesense Server."""
    response = await actual_stopwords_async["company_stopwords"].delete()

    assert response == {"id": "company_stopwords"}
