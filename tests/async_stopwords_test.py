"""Tests for the Stopwords class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.stopwords import Stopwords
from typesense.types.stopword import StopwordSchema, StopwordsRetrieveSchema


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Stopwords object is initialized correctly."""
    stopwords = Stopwords(fake_api_call_async)

    assert_match_object(stopwords.api_call, fake_api_call_async)
    assert_object_lists_match(
        stopwords.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        stopwords.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )

    assert not stopwords.stopwords_sets


def test_get_missing_stopword(fake_stopwords_async: Stopwords) -> None:
    """Test that the Stopwords object can get a missing stopword."""
    stopword = fake_stopwords_async["company_stopwords"]

    assert stopword.stopwords_set_id == "company_stopwords"
    assert_match_object(stopword.api_call, fake_stopwords_async.api_call)
    assert_object_lists_match(
        stopword.api_call.node_manager.nodes,
        fake_stopwords_async.api_call.node_manager.nodes,
    )
    assert_match_object(
        stopword.api_call.config.nearest_node,
        fake_stopwords_async.api_call.config.nearest_node,
    )
    assert stopword._endpoint_path == "/stopwords/company_stopwords"


def test_get_existing_stopword(fake_stopwords_async: Stopwords) -> None:
    """Test that the Stopwords object can get an existing stopword."""
    stopword = fake_stopwords_async["company_stopwords"]
    fetched_stopword = fake_stopwords_async["company_stopwords"]

    assert len(fake_stopwords_async.stopwords_sets) == 1

    assert stopword is fetched_stopword


@pytest.mark.asyncio
async def test_retrieve(fake_stopwords_async: Stopwords, httpx_mock) -> None:
    """Test that the Stopwords object can retrieve stopwords."""
    json_response: StopwordsRetrieveSchema = {
        "stopwords": [
            {
                "id": "company_stopwords",
                "locale": "",
                "stopwords": ["and", "is", "the"],
            },
        ],
    }

    httpx_mock.add_response(
        url="http://nearest:8108/stopwords",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_stopwords_async.retrieve()

    assert len(response) == 1
    assert response["stopwords"][0] == json_response["stopwords"][0]
    assert response == json_response


@pytest.mark.asyncio
async def test_create(fake_stopwords_async: Stopwords, httpx_mock) -> None:
    """Test that the Stopwords object can create a stopword."""
    json_response: StopwordSchema = {
        "id": "company_stopwords",
        "locale": "",
        "stopwords": ["and", "is", "the"],
    }

    httpx_mock.add_response(
        url="http://nearest:8108/stopwords/company_stopwords",
        method="PUT",
        json=json_response,
        status_code=201,
    )

    await fake_stopwords_async.upsert(
        "company_stopwords",
        {"stopwords": ["and", "is", "the"]},
    )

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "PUT"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/stopwords/company_stopwords"
    )
    assert (
        httpx_mock.get_requests()[0].read().decode()
        == '{"stopwords": ["and", "is", "the"]}'
    )


@pytest.mark.asyncio
async def test_actual_create(
    actual_stopwords_async: Stopwords, delete_all_stopwords_async: None
) -> None:
    """Test that the Stopwords object can create an stopword on Typesense Server."""
    response = await actual_stopwords_async.upsert(
        "company_stopwords",
        {"stopwords": ["and", "is", "the"]},
    )

    assert response == {
        "id": "company_stopwords",
        "stopwords": ["and", "is", "the"],
    }


@pytest.mark.asyncio
async def test_actual_update(
    actual_stopwords_async: Stopwords,
    delete_all_stopwords_async: None,
) -> None:
    """Test that the Stopwords object can update an stopword on Typesense Server."""
    create_response = await actual_stopwords_async.upsert(
        "company_stopwords",
        {"stopwords": ["and", "is", "the"]},
    )

    assert create_response == {
        "id": "company_stopwords",
        "stopwords": ["and", "is", "the"],
    }

    update_response = await actual_stopwords_async.upsert(
        "company_stopwords",
        {"stopwords": ["and", "is", "other"]},
    )

    assert update_response == {
        "id": "company_stopwords",
        "stopwords": ["and", "is", "other"],
    }


@pytest.mark.asyncio
async def test_actual_retrieve(
    delete_all_stopwords_async: None,
    create_stopword_async: None,
    actual_stopwords_async: Stopwords,
) -> None:
    """Test that the Stopwords object can retrieve an stopword from Typesense Server."""
    response = await actual_stopwords_async.retrieve()

    assert len(response["stopwords"]) == 1
    assert_to_contain_object(
        response["stopwords"][0],
        {
            "id": "company_stopwords",
            "stopwords": ["and", "is", "the"],
        },
    )
