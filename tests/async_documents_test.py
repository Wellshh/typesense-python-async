"""Tests for the Documents class."""

import json
import logging
import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

import pytest
from pytest_mock import MockFixture

from tests.fixtures.document_fixtures import Companies
from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_keys,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.documents import Documents
from typesense.exceptions import InvalidParameter, TypesenseClientError


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Documents object is initialized correctly."""
    documents = Documents(fake_api_call_async, "companies")

    assert_match_object(documents.api_call, fake_api_call_async)
    assert_object_lists_match(
        documents.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        documents.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )

    assert not documents.documents


def test_get_missing_document(fake_async_documents: Documents) -> None:
    """Test that the Documents object can get a missing document."""
    document = fake_async_documents["1"]

    assert_match_object(document.api_call, fake_async_documents.api_call)
    assert_object_lists_match(
        document.api_call.node_manager.nodes,
        fake_async_documents.api_call.node_manager.nodes,
    )
    assert_match_object(
        document.api_call.config.nearest_node,
        fake_async_documents.api_call.config.nearest_node,
    )
    assert document._endpoint_path == "/collections/companies/documents/1"


def test_get_existing_document(fake_async_documents: Documents) -> None:
    """Test that the Documents object can get an existing document."""
    document = fake_async_documents["1"]
    fetched_document = fake_async_documents["1"]

    assert len(fake_async_documents.documents) == 1

    assert document is fetched_document


@pytest.mark.asyncio
async def test_create(
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    mocker: MockFixture,
) -> None:
    """Test that the Documents object can create a document on Typesense server."""
    company: Companies = {
        "company_name": "Typesense",
        "id": "1",
        "num_employees": 25,
    }
    spy = mocker.spy(actual_api_call_async, "post")
    response = await actual_async_documents.create(company)
    expected = company
    assert response == expected
    spy.assert_called_once_with(
        "/collections/companies/documents/",
        body=company,
        params={"action": "create"},
        as_json=True,
        entity_type=typing.Dict[str, str],
    )


@pytest.mark.asyncio
async def test_upsert(
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    mocker: MockFixture,
) -> None:
    """Test that the Documents object can upsert a document on Typesense server."""
    company: Companies = {
        "company_name": "company",
        "id": "0",
        "num_employees": 10,
    }
    spy = mocker.spy(actual_api_call_async, "post")
    response = await actual_async_documents.upsert(company)

    assert response == company
    spy.assert_called_once_with(
        "/collections/companies/documents/",
        body=company,
        params={"action": "upsert"},
        as_json=True,
        entity_type=typing.Dict[str, str],
    )

    updated_company: Companies = {
        "company_name": "company_updated",
        "id": "0",
        "num_employees": 10,
    }

    response_update = await actual_async_documents.upsert(
        updated_company,
        {"action": "update"},
    )

    assert response_update == updated_company
    assert spy.call_count == 2
    spy.assert_called_with(
        "/collections/companies/documents/",
        body=updated_company,
        params={"action": "upsert"},
        as_json=True,
        entity_type=typing.Dict[str, str],
    )


@pytest.mark.asyncio
async def test_update(
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Documents object can update a document on Typesense server."""
    response = await actual_async_documents.update(
        {"company_name": "company_updated", "num_employees": 10},
        {"filter_by": "company_name:company"},
    )

    assert response == {"num_updated": 1}


@pytest.mark.asyncio
async def test_create_many(
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    mocker: MockFixture,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that the Documents object can create many documents on Typesense server."""
    companies: typing.List[Companies] = [
        {
            "company_name": "Typesense",
            "id": "1",
            "num_employees": 25,
        },
        {
            "company_name": "Typesense",
            "id": "2",
            "num_employees": 25,
        },
    ]
    with caplog.at_level(logging.WARNING):
        response = await actual_async_documents.create_many(companies)
        expected = [{"success": True} for _ in companies]
        assert response == expected
        assert "`create_many` is deprecated: please use `import_`." in caplog.text


@pytest.mark.asyncio
async def test_export(
    actual_async_documents: Documents[Companies],
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Documents object can export a document from Typesense server."""
    response = await actual_async_documents.export()
    assert response == '{"company_name":"Company","id":"0","num_employees":10}'


@pytest.mark.asyncio
async def test_delete(
    actual_async_documents: Documents[Companies],
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Documents object can delete a document from Typesense server."""
    response = await actual_async_documents.delete(
        {"filter_by": "company_name:Company"}
    )
    assert response == {"num_deleted": 1}


@pytest.mark.asyncio
async def test_delete_ignore_missing(
    actual_async_documents: Documents[Companies],
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Documents object can ignore a missing document from Typesense server."""
    response = await actual_async_documents.delete(
        {"filter_by": "company_name:missing", "ignore_not_found": True},
    )
    assert response == {"num_deleted": 0}


@pytest.mark.asyncio
async def test_import_fail(
    generate_companies: typing.List[Companies],
    actual_async_documents: Documents[Companies],
    delete_all_async: None,
    create_collection_async: None,
    mocker: MockFixture,
) -> None:
    """Test that the Documents object doesn't throw an error when importing documents."""
    wrong_company: Companies = {"company_name": "Wrong", "id": "0", "num_employees": 0}
    companies = generate_companies + [wrong_company]
    request_spy = mocker.spy(actual_async_documents, "_bulk_import")
    response = await actual_async_documents.import_(companies)

    expected: typing.List[typing.Dict[str, typing.Union[str, bool, int]]] = [
        {"success": True} for _ in generate_companies
    ]
    expected.append(
        {
            "code": 409,
            "error": "A document with id 0 already exists.",
            "success": False,
        },
    )
    assert request_spy.call_count == 1
    assert response == expected


@pytest.mark.asyncio
async def test_import_empty(
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Documents object throws when importing an empty list of documents."""
    with pytest.raises(TypesenseClientError):
        await actual_async_documents.import_(documents=[])


@pytest.mark.asyncio
async def test_import_json_fail(
    actual_async_documents: Documents[Companies],
    generate_companies: typing.List[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    mocker: MockFixture,
) -> None:
    """Test that the Documents object throws when importing invalid JSON."""
    mocker.patch(
        "json.loads",
        side_effect=json.JSONDecodeError("Expecting value", "doc", 0),
    )

    with pytest.raises(TypesenseClientError):
        await actual_async_documents.import_(generate_companies)


@pytest.mark.asyncio
async def test_import_batch_size(
    generate_companies: typing.List[Companies],
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    mocker: MockFixture,
) -> None:
    """Test that the Documents object can import documents in batches."""
    batch_size = 5
    import_spy = mocker.spy(actual_async_documents, "import_")
    batch_import_spy = mocker.spy(actual_async_documents, "_bulk_import")
    request_spy = mocker.spy(actual_api_call_async, "post")
    response = await actual_async_documents.import_(
        generate_companies, batch_size=batch_size
    )

    expected = [{"success": True} for _ in generate_companies]
    assert import_spy.call_count == 1
    assert batch_import_spy.call_count == len(generate_companies) // batch_size
    assert request_spy.call_count == len(generate_companies) // batch_size
    assert response == expected


@pytest.mark.asyncio
async def test_import_return_docs(
    generate_companies: typing.List[Companies],
    actual_async_documents: Documents[Companies],
    mocker: MockFixture,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Documents object can return documents when importing."""
    request_spy = mocker.spy(actual_async_documents, "_bulk_import")
    response = await actual_async_documents.import_(
        generate_companies, {"return_doc": True}
    )
    expected = [
        {"success": True, "document": company} for company in generate_companies
    ]

    assert request_spy.call_count == 1
    assert response == expected


@pytest.mark.asyncio
async def test_import_return_ids(
    generate_companies: typing.List[Companies],
    actual_async_documents: Documents[Companies],
    mocker: MockFixture,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Documents object can return document IDs when importing."""
    request_spy = mocker.spy(actual_async_documents, "_bulk_import")
    response = await actual_async_documents.import_(
        generate_companies, {"return_id": True}
    )
    expected = [
        {"success": True, "id": company.get("id")} for company in generate_companies
    ]
    assert request_spy.call_count == 1
    assert response == expected


@pytest.mark.asyncio
async def test_import_return_ids_and_docs(
    generate_companies: typing.List[Companies],
    actual_async_documents: Documents[Companies],
    mocker: MockFixture,
    delete_all_async: None,
    create_collection_async: None,
) -> None:
    """Test that the Documents object can return document IDs and documents when importing."""
    request_spy = mocker.spy(actual_async_documents, "_bulk_import")
    response = await actual_async_documents.import_(
        generate_companies,
        {"return_id": True, "return_doc": True},
    )
    expected = [
        {"success": True, "document": company, "id": company.get("id")}
        for company in generate_companies
    ]
    assert request_spy.call_count == 1
    assert response == expected


@pytest.mark.asyncio
async def test_import_jsonl(
    generate_companies: typing.List[Companies],
    actual_async_documents: Documents[Companies],
    delete_all_async: None,
    create_collection_async: None,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that the Documents object can import documents in JSONL format."""
    companies_in_jsonl_format = "\n".join(
        [
            "".join(
                [
                    '{"id": "',
                    company["id"],
                    '", ',
                    '"company_name": "',
                    company["company_name"],
                    '", ',
                    '"num_employees": ',
                    str(company["num_employees"]),
                    "}",
                ],
            )
            for company in generate_companies
        ],
    )

    expected = "\n".join(['{"success":true}' for _ in generate_companies])

    with caplog.at_level(logging.WARNING):
        response = await actual_async_documents.import_jsonl(companies_in_jsonl_format)
        assert response == expected
        assert "`import_jsonl` is deprecated: please use `import_`." in caplog.text


@pytest.mark.asyncio
async def test_search(
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Documents object can search for documents on Typesense server."""
    response = await actual_async_documents.search(
        {
            "q": "com",
            "query_by": "company_name",
        },
    )

    assert_to_contain_keys(
        response,
        [
            "facet_counts",
            "found",
            "hits",
            "page",
            "out_of",
            "request_params",
            "search_time_ms",
            "search_cutoff",
        ],
    )

    assert_to_contain_keys(
        response.get("hits")[0],
        ["document", "highlights", "highlight", "text_match", "text_match_info"],
    )


@pytest.mark.asyncio
async def test_search_array(
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the SearchParameters can have arrays that are concatenated before request."""
    response = await actual_async_documents.search(
        {
            "q": "com",
            "query_by": ["company_name"],
        },
    )

    assert_to_contain_keys(
        response,
        [
            "facet_counts",
            "found",
            "hits",
            "page",
            "out_of",
            "request_params",
            "search_time_ms",
            "search_cutoff",
        ],
    )

    assert_to_contain_keys(
        response.get("hits")[0],
        ["document", "highlights", "highlight", "text_match", "text_match_info"],
    )


@pytest.mark.asyncio
async def test_search_invalid_parameters(
    actual_async_documents: Documents[Companies],
    actual_api_call_async: AsyncApiCall,
    delete_all_async: None,
    create_collection_async: None,
    create_document_async: None,
) -> None:
    """Test that the Documents object throws when invalid parameters are passed to search."""
    with pytest.raises(InvalidParameter):
        await actual_async_documents.search(
            {
                "q": "com",
                "query_by": "company_name",
                "invalid": [
                    Companies(company_name="", id="", num_employees=0),
                ],
            },
        )

    with pytest.raises(InvalidParameter):
        await actual_async_documents.search(
            {
                "q": "com",
                "query_by": "company_name",
                "invalid": Companies(company_name="", id="", num_employees=0),
            },
        )
