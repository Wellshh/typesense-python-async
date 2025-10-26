"""Tests for stemming."""

import pytest

from typesense.async_client.stemming import Stemming


@pytest.mark.asyncio
async def test_actual_upsert(
    actual_stemming_async: Stemming,
) -> None:
    """Test that it can upsert a stemming dictionary to Typesense Server."""
    response = await actual_stemming_async.dictionaries.upsert(
        "set_1",
        [{"word": "running", "root": "run"}, {"word": "fishing", "root": "fish"}],
    )

    assert response == [
        {"word": "running", "root": "run"},
        {"word": "fishing", "root": "fish"},
    ]


@pytest.mark.asyncio
async def test_actual_retrieve_many(
    actual_stemming_async: Stemming,
) -> None:
    """Test that it can retrieve all stemming dictionaries from Typesense Server."""
    await actual_stemming_async.dictionaries.upsert(
        "set_1",
        [{"word": "running", "root": "run"}, {"word": "fishing", "root": "fish"}],
    )
    response = await actual_stemming_async.dictionaries.retrieve()
    assert response == {"dictionaries": ["set_1"]}
