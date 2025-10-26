"""Fixtures for the NL search model tests."""

import os

import httpx
import pytest
import pytest_asyncio
import requests
from dotenv import load_dotenv

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.nl_search_model import NLSearchModel as AsyncNLSearchModel
from typesense.async_client.nl_search_models import (
    NLSearchModels as AsyncNLSearchModels,
)
from typesense.nl_search_model import NLSearchModel
from typesense.nl_search_models import NLSearchModels

load_dotenv()


@pytest.fixture(scope="function", name="delete_all_nl_search_models")
def clear_typesense_nl_search_models() -> None:
    """Remove all nl_search_models from the Typesense server."""
    url = "http://localhost:8108/nl_search_models"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    # Get the list of models
    response = requests.get(url, headers=headers, timeout=3)
    response.raise_for_status()

    nl_search_models = response.json()

    # Delete each NL search model
    for nl_search_model in nl_search_models:
        model_id = nl_search_model.get("id")
        delete_url = f"{url}/{model_id}"
        delete_response = requests.delete(delete_url, headers=headers, timeout=3)
        delete_response.raise_for_status()


@pytest.fixture(scope="function", name="create_nl_search_model")
def create_nl_search_model_fixture() -> str:
    """Create an NL search model in the Typesense server."""
    url = "http://localhost:8108/nl_search_models"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    nl_search_model_data = {
        "api_key": os.environ.get("OPEN_AI_KEY", "test-api-key"),
        "max_bytes": 16384,
        "model_name": "openai/gpt-3.5-turbo",
        "system_prompt": "This is a system prompt for NL search",
    }

    response = requests.post(
        url,
        headers=headers,
        json=nl_search_model_data,
        timeout=3,
    )

    response.raise_for_status()

    model_id: str = response.json()["id"]
    return model_id


@pytest.fixture(scope="function", name="fake_nl_search_models")
def fake_nl_search_models_fixture(fake_api_call: ApiCall) -> NLSearchModels:
    """Return an NLSearchModels object with test values."""
    return NLSearchModels(fake_api_call)


@pytest.fixture(scope="function", name="fake_nl_search_model")
def fake_nl_search_model_fixture(fake_api_call: ApiCall) -> NLSearchModel:
    """Return an NLSearchModel object with test values."""
    return NLSearchModel(fake_api_call, "nl_search_model_id")


@pytest.fixture(scope="function", name="actual_nl_search_models")
def actual_nl_search_models_fixture(
    actual_api_call: ApiCall,
) -> NLSearchModels:
    """Return an NLSearchModels object using a real API."""
    return NLSearchModels(actual_api_call)


@pytest_asyncio.fixture(loop_scope="function", name="delete_all_nl_search_models_async")
async def clear_typesense_nl_search_models_async() -> None:
    """Remove all nl_search_models from the Typesense server asynchronously."""
    url = "http://localhost:8108/nl_search_models"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        nl_search_models = response.json()

        for nl_search_model in nl_search_models:
            model_id = nl_search_model.get("id")
            delete_url = f"{url}/{model_id}"
            delete_response = await client.delete(
                delete_url, headers=headers, timeout=3
            )
            delete_response.raise_for_status()


@pytest_asyncio.fixture(loop_scope="function", name="create_nl_search_model_async")
async def create_nl_search_model_fixture_async() -> str:
    """Create an NL search model in the Typesense server asynchronously."""
    url = "http://localhost:8108/nl_search_models"
    headers = {"X-TYPESENSE-API-KEY": "xyz"}
    nl_search_model_data = {
        "api_key": os.environ.get("OPEN_AI_KEY", "test-api-key"),
        "max_bytes": 16384,
        "model_name": "openai/gpt-3.5-turbo",
        "system_prompt": "This is a system prompt for NL search",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=nl_search_model_data,
            timeout=3,
        )
        response.raise_for_status()
        model_id: str = response.json()["id"]
        return model_id


@pytest_asyncio.fixture(loop_scope="function", name="fake_nl_search_models_async")
async def fake_nl_search_models_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncNLSearchModels:
    """Return an AsyncNLSearchModels object with test values."""
    return AsyncNLSearchModels(fake_api_call_async)


@pytest_asyncio.fixture(loop_scope="function", name="fake_nl_search_model_async")
async def fake_nl_search_model_fixture_async(
    fake_api_call_async: AsyncApiCall,
) -> AsyncNLSearchModel:
    """Return an AsyncNLSearchModel object with test values."""
    return AsyncNLSearchModel(fake_api_call_async, "nl_search_model_id")


@pytest_asyncio.fixture(loop_scope="function", name="actual_nl_search_models_async")
async def actual_nl_search_models_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncNLSearchModels:
    """Return an AsyncNLSearchModels object using a real API."""
    return AsyncNLSearchModels(actual_api_call_async)
