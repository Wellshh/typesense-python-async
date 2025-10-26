"""Tests for the NLSearchModel class."""

from __future__ import annotations

import pytest
from dotenv import load_dotenv

from tests.utils.object_assertions import (
    assert_match_object,
    assert_object_lists_match,
    assert_to_contain_keys,
)
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.nl_search_model import NLSearchModel
from typesense.async_client.nl_search_models import NLSearchModels

load_dotenv()


def test_init(fake_api_call_async: AsyncApiCall) -> None:
    """Test that the NLSearchModel object is initialized correctly."""
    nl_search_model = NLSearchModel(
        fake_api_call_async,
        "nl_search_model_id",
    )

    assert nl_search_model.model_id == "nl_search_model_id"
    assert_match_object(nl_search_model.api_call, fake_api_call_async)
    assert_object_lists_match(
        nl_search_model.api_call.node_manager.nodes,
        fake_api_call_async.node_manager.nodes,
    )
    assert_match_object(
        nl_search_model.api_call.config.nearest_node,
        fake_api_call_async.config.nearest_node,
    )
    assert nl_search_model._endpoint_path == "/nl_search_models/nl_search_model_id"


@pytest.mark.open_ai
@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_nl_search_models_async: NLSearchModels,
    delete_all_nl_search_models_async: None,
    create_nl_search_model_async: str,
) -> None:
    """Test it can retrieve an NL search model from Typesense Server."""
    response = await actual_nl_search_models_async[
        create_nl_search_model_async
    ].retrieve()

    assert_to_contain_keys(
        response,
        ["id", "model_name", "system_prompt", "max_bytes", "api_key"],
    )
    assert response.get("id") == create_nl_search_model_async


@pytest.mark.open_ai
@pytest.mark.asyncio
async def test_actual_update(
    actual_nl_search_models_async: NLSearchModels,
    delete_all_nl_search_models_async: None,
    create_nl_search_model_async: str,
) -> None:
    """Test that it can update an NL search model from Typesense Server."""
    response = await actual_nl_search_models_async[create_nl_search_model_async].update(
        {"system_prompt": "This is a new system prompt for NL search"},
    )

    assert_to_contain_keys(
        response,
        [
            "id",
            "model_name",
            "system_prompt",
            "max_bytes",
            "api_key",
        ],
    )

    assert response.get("system_prompt") == "This is a new system prompt for NL search"
    assert response.get("id") == create_nl_search_model_async


@pytest.mark.open_ai
@pytest.mark.asyncio
async def test_actual_delete(
    actual_nl_search_models_async: NLSearchModels,
    delete_all_nl_search_models_async: None,
    create_nl_search_model_async: str,
) -> None:
    """Test that it can delete an NL search model from Typesense Server."""
    response = await actual_nl_search_models_async[
        create_nl_search_model_async
    ].delete()

    assert_to_contain_keys(
        response,
        ["id"],
    )

    assert response.get("id") == create_nl_search_model_async
