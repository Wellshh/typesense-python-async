"""Tests for stemming."""

from typesense.async_client.stemming import Stemming


def test_actual_upsert(
    actual_stemming_async: Stemming,
) -> None:
    """Test that it can upsert a stemming dictionary to Typesense Server."""
    assert actual_stemming_async.dictionaries is not None
