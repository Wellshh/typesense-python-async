"""Tests for the AnalyticsRules class."""

from __future__ import annotations

import pytest

from tests.utils.object_assertions import assert_match_object, assert_object_lists_match
from typesense.async_client.analytics_rules import AnalyticsRules
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.types.analytics_rule import (
    RuleCreateSchemaForQueries,
    RulesRetrieveSchema,
)


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the AnalyticsRules object is initialized correctly."""
    analytics_rules = AnalyticsRules(fake_api_call_async)

    assert_match_object(analytics_rules.api_call, fake_api_call_async)
    assert_object_lists_match(
        analytics_rules.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        analytics_rules.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )

    assert not analytics_rules.rules


def test_get_missing_analytics_rule(fake_analytics_rules_async: AnalyticsRules) -> None:
    """Test that the AnalyticsRules object can get a missing analytics_rule."""
    analytics_rule = fake_analytics_rules_async["company_analytics_rule"]

    assert analytics_rule.rule_id == "company_analytics_rule"
    assert_match_object(analytics_rule.api_call, fake_analytics_rules_async.api_call)
    assert_object_lists_match(
        analytics_rule.api_call.node_manager.nodes,
        fake_analytics_rules_async.api_call.node_manager.nodes,
    )
    assert_match_object(
        analytics_rule.api_call.config.nearest_node,
        fake_analytics_rules_async.api_call.config.nearest_node,
    )
    assert analytics_rule._endpoint_path == "/analytics/rules/company_analytics_rule"


def test_get_existing_analytics_rule(
    fake_analytics_rules_async: AnalyticsRules,
) -> None:
    """Test that the AnalyticsRules object can get an existing analytics_rule."""
    analytics_rule = fake_analytics_rules_async["company_analytics_rule"]
    fetched_analytics_rule = fake_analytics_rules_async["company_analytics_rule"]

    assert len(fake_analytics_rules_async.rules) == 1

    assert analytics_rule is fetched_analytics_rule


@pytest.mark.asyncio
async def test_retrieve(fake_analytics_rules_async: AnalyticsRules, httpx_mock) -> None:
    """Test that the AnalyticsRules object can retrieve analytics_rules."""
    json_response: RulesRetrieveSchema = {
        "rules": [
            {
                "name": "company_analytics_rule",
                "params": {
                    "destination": {
                        "collection": "companies_queries",
                    },
                    "source": {"collections": ["companies"]},
                },
                "type": "nohits_queries",
            },
        ],
    }

    httpx_mock.add_response(
        url="http://nearest:8108/analytics/rules",
        method="GET",
        json=json_response,
        status_code=200,
    )

    response = await fake_analytics_rules_async.retrieve()

    assert len(response) == 1
    assert response["rules"][0] == json_response.get("rules")[0]
    assert response == json_response


@pytest.mark.asyncio
async def test_create(fake_analytics_rules_async: AnalyticsRules, httpx_mock) -> None:
    """Test that the AnalyticsRules object can create a analytics_rule."""
    json_response: RuleCreateSchemaForQueries = {
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
        url="http://nearest:8108/analytics/rules",
        method="POST",
        json=json_response,
        status_code=201,
    )

    await fake_analytics_rules_async.create(
        rule={
            "params": {
                "destination": {
                    "collection": "companies_queries",
                },
                "source": {"collections": ["companies"]},
            },
            "type": "nohits_queries",
            "name": "company_analytics_rule",
        },
    )

    assert len(httpx_mock.get_requests()) == 1
    assert httpx_mock.get_requests()[0].method == "POST"
    assert (
        str(httpx_mock.get_requests()[0].url) == "http://nearest:8108/analytics/rules"
    )
    assert (
        httpx_mock.get_requests()[0].read().decode()
        == '{"params": {"destination": {"collection": "companies_queries"}, "source": {"collections": ["companies"]}}, "type": "nohits_queries", "name": "company_analytics_rule"}'
    )


@pytest.mark.asyncio
async def test_actual_create(
    actual_analytics_rules_async: AnalyticsRules,
    delete_all_async: None,
    delete_all_analytics_rules_async: None,
    create_collection_async: None,
    create_query_collection_async: None,
) -> None:
    """Test that the AnalyticsRules object can create an analytics_rule on Typesense Server."""
    response = await actual_analytics_rules_async.create(
        rule={
            "name": "company_analytics_rule",
            "type": "nohits_queries",
            "params": {
                "source": {
                    "collections": ["companies"],
                },
                "destination": {"collection": "companies_queries"},
            },
        },
    )

    assert response == {
        "name": "company_analytics_rule",
        "type": "nohits_queries",
        "params": {
            "source": {"collections": ["companies"]},
            "destination": {"collection": "companies_queries"},
        },
    }


@pytest.mark.asyncio
async def test_actual_update(
    actual_analytics_rules_async: AnalyticsRules,
    delete_all_async: None,
    delete_all_analytics_rules_async: None,
    create_analytics_rule_async: None,
) -> None:
    """Test that the AnalyticsRules object can update an analytics_rule on Typesense Server."""
    response = await actual_analytics_rules_async.upsert(
        "company_analytics_rule",
        {
            "type": "popular_queries",
            "params": {
                "source": {
                    "collections": ["companies"],
                },
                "destination": {"collection": "companies_queries"},
            },
        },
    )

    assert response == {
        "name": "company_analytics_rule",
        "type": "popular_queries",
        "params": {
            "source": {"collections": ["companies"]},
            "destination": {"collection": "companies_queries"},
        },
    }


@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_analytics_rules_async: AnalyticsRules,
    delete_all_async: None,
    delete_all_analytics_rules_async: None,
    create_analytics_rule_async: None,
) -> None:
    """Test that the AnalyticsRules object can retrieve the rules from Typesense Server."""
    response = await actual_analytics_rules_async.retrieve()
    assert len(response["rules"]) == 1
    assert_match_object(
        response["rules"][0],
        {
            "name": "company_analytics_rule",
            "params": {
                "destination": {"collection": "companies_queries"},
                "limit": 1000,
                "source": {"collections": ["companies"]},
            },
            "type": "nohits_queries",
        },
    )
