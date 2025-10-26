"""Tests for the AnalyticsRule class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import assert_match_object, assert_object_lists_match
from typesense.async_client.analytics_rule import AnalyticsRule
from typesense.async_client.analytics_rules import AnalyticsRules
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.types.analytics_rule import RuleDeleteSchema, RuleSchemaForQueries


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the AnalyticsRule object is initialized correctly."""
    analytics_rule = AnalyticsRule(fake_api_call_async, "company_analytics_rule")

    assert analytics_rule.rule_id == "company_analytics_rule"
    assert_match_object(analytics_rule.api_call, fake_api_call_async)
    assert_object_lists_match(
        analytics_rule.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        analytics_rule.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert analytics_rule._endpoint_path == "/analytics/rules/company_analytics_rule"


@pytest.mark.asyncio
async def test_retrieve(fake_analytics_rule_async: AnalyticsRule, httpx_mock) -> None:
    """Test that the AnalyticsRule object can retrieve an analytics_rule."""
    json_response: RuleSchemaForQueries = {
        "name": "company_analytics_rule",
        "params": {
            "destination": {
                "collection": "companies_queries",
            },
            "source": {"collections": ["companies"]},
        },
        "type": "nohits_queries",
    }

    httpx_mock.add_response(
        url="http://nearest:8108/analytics/rules/company_analytics_rule",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_analytics_rule_async.retrieve()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "GET"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/analytics/rules/company_analytics_rule"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_delete(fake_analytics_rule_async: AnalyticsRule, httpx_mock) -> None:
    """Test that the AnalyticsRule object can delete an analytics_rule."""
    json_response: RuleDeleteSchema = {
        "name": "company_analytics_rule",
    }
    httpx_mock.add_response(
        url="http://nearest:8108/analytics/rules/company_analytics_rule",
        method="DELETE",
        json=json_response,
        status_code=200,
    )

    response = await fake_analytics_rule_async.delete()

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "DELETE"
    assert (
        str(httpx_mock.get_requests()[0].url)
        == "http://nearest:8108/analytics/rules/company_analytics_rule"
    )
    assert response == json_response


@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_analytics_rules_async: AnalyticsRules,
    delete_all_async: None,
    delete_all_analytics_rules_async: None,
    create_analytics_rule_async: None,
) -> None:
    """Test that the AnalyticsRule object can retrieve a rule from Typesense Server."""
    response = await actual_analytics_rules_async["company_analytics_rule"].retrieve()

    expected: RuleSchemaForQueries = {
        "name": "company_analytics_rule",
        "params": {
            "destination": {"collection": "companies_queries"},
            "limit": 1000,
            "source": {"collections": ["companies"]},
        },
        "type": "nohits_queries",
    }

    assert response == expected


@pytest.mark.asyncio
async def test_actual_delete(
    actual_analytics_rules_async: AnalyticsRules,
    delete_all_async: None,
    delete_all_analytics_rules_async: None,
    create_analytics_rule_async: None,
) -> None:
    """Test that the AnalyticsRule object can delete a rule from Typesense Server."""
    response = await actual_analytics_rules_async["company_analytics_rule"].delete()

    expected: RuleDeleteSchema = {
        "name": "company_analytics_rule",
    }
    assert response == expected
