"""Tests for the Analytics class."""

from tests.utils.object_assertions import assert_match_object, assert_object_lists_match
from typesense.async_client.analytics import Analytics
from typesense.async_client.async_api_call import AsyncApiCall


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the Analytics object is initialized correctly."""
    analytics = Analytics(fake_api_call_async)

    assert_match_object(analytics.rules.api_call, fake_api_call_async)
    assert_object_lists_match(
        analytics.rules.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        analytics.rules.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )

    assert not analytics.rules.rules
