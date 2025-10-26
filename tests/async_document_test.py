"""Tests for the Document class."""

from __future__ import annotations

import pytest

from tests.fixtures.document_fixtures import Companies
from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_object,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.document import Document
from typesense.async_client.documents import Documents
from typesense.exceptions import ObjectNotFound


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Document object is initialized correctly."""
    document = Document(fake_api_call_async, "companies", "0")

    assert document.document_id == "0"
    assert document.collection_name == "companies"
    assert_match_object(document.api_call, fake_api_call_async)
    assert_object_lists_match(
        document.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        document.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert document._endpoint_path == "/collections/companies/documents/0"


@pytest.mark.asyncio
async def test_retrieve(fake_async_document: Document, httpx_mock) -> None:
    """Test that the Document object can retrieve an document."""
    json_response: Companies = {
        "company_name": "Company",
        "id": "0",
        "num_employees": 10,
    }

    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/documents/0",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_async_document.retrieve()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "GET"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/collections/companies/documents/0"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_delete(fake_async_document: Document, httpx_mock) -> None:
    """Test that the Document object can delete an document."""
    json_response: Companies = {
        "company_name": "Company",
        "id": "0",
        "num_employees": 10,
    }
    httpx_mock.add_response(
        url="http://nearest:8108/collections/companies/documents/0",
        method="DELETE",
        json=json_response,
        status_code=200,
    )

    response = await fake_async_document.delete()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "DELETE"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/collections/companies/documents/0"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_actual_update(
    actual_async_documents: Documents,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Document object can update an document on Typesense Server."""
    response = await actual_async_documents["0"].update(
        {"company_name": "Company", "num_employees": 20},
        {
            "action": "update",
        },
    )

    assert_to_contain_object(
        response,
        {"id": "0", "company_name": "Company", "num_employees": 20},
    )


@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_async_documents: Documents,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Document object can retrieve an document from Typesense Server."""
    response = await actual_async_documents["0"].retrieve()

    assert_to_contain_object(
        response,
        {"id": "0", "company_name": "Company", "num_employees": 10},
    )


@pytest.mark.asyncio
async def test_actual_delete(
    actual_async_documents: Documents,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Document object can delete an document from Typesense Server."""
    response = await actual_async_documents["0"].delete()

    assert response == {
        "id": "0",
        "company_name": "Company",
        "num_employees": 10,
    }


@pytest.mark.asyncio
async def test_actual_delete_non_existent(
    actual_async_documents: Documents,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Document object can delete an document from Typesense Server."""
    with pytest.raises(ObjectNotFound):
        await actual_async_documents["1"].delete()


@pytest.mark.asyncio
async def test_actual_delete_non_existent_ignore_not_found(
    actual_async_documents: Documents,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Document object can delete an document from Typesense Server."""
    response = await actual_async_documents["1"].delete(
        delete_parameters={"ignore_not_found": True},
    )

    assert response == {"id": "1"}
