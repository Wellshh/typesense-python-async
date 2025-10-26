"""Fixtures for the Metrics class tests."""

import pytest
import pytest_asyncio

from typesense.api_call import ApiCall
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.metrics import Metrics as AsyncMetrics
from typesense.metrics import Metrics


@pytest.fixture(scope="function", name="actual_metrics")
def actual_debug_fixture(actual_api_call: ApiCall) -> Metrics:
    """Return a Debug object using a real API."""
    return Metrics(actual_api_call)


@pytest_asyncio.fixture(loop_scope="function", name="actual_metrics_async")
async def actual_debug_fixture_async(
    actual_api_call_async: AsyncApiCall,
) -> AsyncMetrics:
    """Return an AsyncMetrics object using a real API."""
    return AsyncMetrics(actual_api_call_async)
