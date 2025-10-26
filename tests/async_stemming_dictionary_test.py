"""Tests for stemming."""

import pytest

from typesense.async_client.stemming import Stemming


@pytest.mark.asyncio
async def test_actual_retrieve(
    actual_stemming_async: Stemming,
) -> None:
    """Test that it can retrieve a single stemming dictionary from Typesense Server."""
    await actual_stemming_async.dictionaries.upsert(
        "set_1",
        [{"word": "running", "root": "run"}, {"word": "fishing", "root": "fish"}],
    )
    response = await actual_stemming_async.dictionaries["set_1"].retrieve()
    assert response == {
        "id": "set_1",
        "words": [
            {"word": "running", "root": "run"},
            {"word": "fishing", "root": "fish"},
        ],
    }
