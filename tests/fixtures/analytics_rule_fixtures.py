"""Fixtures for the Analytics Rules tests."""

import httpx
import pytest
import pytest_asyncio
import requests

from typesense.analytics_rule import AnalyticsRule
from typesense.analytics_rules import AnalyticsRules
from typesense.api_call import ApiCall
from typesense.async_client.analytics_rule import AnalyticsRule as AsyncAnalyticsRule
from typesense.async_client.analytics_rules import AnalyticsRules as AsyncAnalyticsRules
from typesense.async_client.async_api_call import AsyncApiCall


@pytest.fixture(scope="function", name="delete_all_analytics_rules")
def clear_typesense_analytics_rules() -> None:
    """Remove all analytics_rules from the Typesense server."""
    url = "http://localhost:8108/analytics/rules"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    # Get the list of rules
    response = requests.get(url, headers=headers, timeout=3)
    response.raise_for_status()
    analytics_rules = response.json()

    # Delete each analytics_rule
    for analytics_rule_set in analytics_rules["rules"]:
        analytics_rule_id = analytics_rule_set.get("name")
        delete_url = f"{url}/{analytics_rule_id}"
        delete_response = requests.delete(delete_url, headers=headers, timeout=3)
        delete_response.raise_for_status()


@pytest.fixture(scope="function", name="create_analytics_rule")
def create_analytics_rule_fixture(
    create_collection: None,
    create_query_collection: None,
) -> None:
    """Create a collection in the Typesense server."""
    url = "http://localhost:8108/analytics/rules"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    analytics_rule_data = {
        "name": "company_analytics_rule",
        "type": "nohits_queries",
        "params": {
            "source": {
                "collections": ["companies"],
            },
            "destination": {"collection": "companies_queries"},
        },
    }

    response = requests.post(url, headers=headers, json=analytics_rule_data, timeout=3)
    response.raise_for_status()


@pytest.fixture(scope="function", name="fake_analytics_rules")
def fake_analytics_rules_fixture(fake_api_call: ApiCall) -> AnalyticsRules:
    """Return a AnalyticsRule object with test values."""
    return AnalyticsRules(fake_api_call)


@pytest.fixture(scope="function", name="actual_analytics_rules")
def actual_analytics_rules_fixture(actual_api_call: ApiCall) -> AnalyticsRules:
    """Return a AnalyticsRules object using a real API."""
    return AnalyticsRules(actual_api_call)


@pytest.fixture(scope="function", name="fake_analytics_rule")
def fake_analytics_rule_fixture(fake_api_call: ApiCall) -> AnalyticsRule:
    """Return a AnalyticsRule object with test values."""
    return AnalyticsRule(fake_api_call, "company_analytics_rule")


@pytest.fixture(scope="function", name="create_query_collection")
def create_query_collection_fixture() -> None:
    """Create a query collection for analytics rules in the Typesense server."""
    url = "http://localhost:8108/collections"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    query_collection_data = {
        "name": "companies_queries",
        "fields": [
            {
                "name": "q",
                "type": "string",
            },
            {
                "name": "count",
                "type": "int32",
            },
        ],
    }

    response = requests.post(
        url,
        headers=headers,
        json=query_collection_data,
        timeout=3,
    )
    response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="delete_all_analytics_rules_async")
async def clear_typesense_analytics_rules_async() -> None:
    """Remove all analytics_rules from the Typesense server asynchronously."""
    url = "http://localhost:8108/analytics/rules"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        analytics_rules = response.json()

        for analytics_rule_set in analytics_rules["rules"]:
            analytics_rule_id = analytics_rule_set.get("name")
            delete_url = f"{url}/{analytics_rule_id}"
            delete_response = await client.delete(
                delete_url, headers=headers, timeout=3
            )
            delete_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="create_query_collection_async")
async def create_query_collection_fixture_async() -> None:
    """Create a query collection for analytics rules in the Typesense server asynchronously."""
    url = "http://localhost:8108/collections"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    query_collection_data = {
        "name": "companies_queries",
        "fields": [
            {
                "name": "q",
                "type": "string",
            },
            {
                "name": "count",
                "type": "int32",
            },
        ],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=query_collection_data,
            timeout=3,
        )
        response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="create_analytics_rule_async")
async def create_analytics_rule_fixture_async(
    create_collection_async: None,
    create_query_collection_async: None,
) -> None:
    """Create a collection in the Typesense server asynchronously."""
    url = "http://localhost:8108/analytics/rules"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    analytics_rule_data = {
        "name": "company_analytics_rule",
        "type": "nohits_queries",
        "params": {
            "source": {
                "collections": ["companies"],
            },
            "destination": {"collection": "companies_queries"},
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers=headers, json=analytics_rule_data, timeout=3
        )
        response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="fake_analytics_rules_async")
async def fake_analytics_rules_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncAnalyticsRules:
    """Return an AsyncAnalyticsRules object with test values."""
    return AsyncAnalyticsRules(fake_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="actual_analytics_rules_async")
async def actual_analytics_rules_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncAnalyticsRules:
    """Return an AsyncAnalyticsRules object using a real API."""
    return AsyncAnalyticsRules(actual_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_analytics_rule_async")
async def fake_analytics_rule_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncAnalyticsRule:
    """Return an AsyncAnalyticsRule object with test values."""
    return AsyncAnalyticsRule(fake_api_call_async, "company_analytics_rule")
