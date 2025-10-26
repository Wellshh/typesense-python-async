"""
This module provides the main asynchronous client interface for interacting with the Typesense API.

It contains the AsyncClient class, which serves as the entry point for all Typesense operations,
integrating various components like collections, multi-search, keys, aliases, analytics, etc.

Classes:
    AsyncClient: The main async client class for interacting with Typesense.

Dependencies:
    - typesense.async_client.aliases: Provides the Aliases class.
    - typesense.async_client.analytics: Provides the Analytics class.
    - typesense.async_client.async_api_call: Provides the AsyncApiCall class for making API requests.
    - typesense.async_client.collection: Provides the Collection class.
    - typesense.async_client.collections: Provides the Collections class.
    - typesense.configuration: Provides Configuration and ConfigDict types.
    - typesense.async_client.conversations_models: Provides the ConversationsModels class.
    - typesense.async_client.debug: Provides the Debug class.
    - typesense.async_client.keys: Provides the Keys class.
    - typesense.async_client.metrics: Provides the Metrics class.
    - typesense.async_client.multi_search: Provides the MultiSearch class.
    - typesense.async_client.operations: Provides the Operations class.
    - typesense.async_client.stopwords: Provides the Stopwords class.
    - typesense.types.document: Provides the DocumentSchema type.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

from typesense.types.document import DocumentSchema

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from typesense.async_client.aliases import Aliases
from typesense.async_client.analytics import Analytics
from typesense.async_client.async_api_call import AsyncApiCall
from typesense.async_client.collection import Collection
from typesense.async_client.collections import Collections
from typesense.configuration import ConfigDict, Configuration
from typesense.async_client.conversations_models import ConversationsModels
from typesense.async_client.debug import Debug
from typesense.async_client.keys import Keys
from typesense.async_client.metrics import Metrics
from typesense.async_client.multi_search import MultiSearch
from typesense.async_client.nl_search_models import NLSearchModels
from typesense.async_client.operations import Operations
from typesense.async_client.stemming import Stemming
from typesense.async_client.stopwords import Stopwords

TDoc = typing.TypeVar("TDoc", bound=DocumentSchema)


class AsyncClient:
    """
    The main async client class for interacting with Typesense.

    This class serves as the entry point for all Typesense operations. It initializes
    and provides access to various components of the Typesense SDK, such as collections,
    multi-search, keys, aliases, analytics, stemming, operations, debug, stopwords,
    and conversation models.

    Attributes:
        config (Configuration): The configuration object for the Typesense client.
        api_call (AsyncApiCall): The AsyncApiCall instance for making API requests.
        collections (Collections[DocumentSchema]): Instance for managing collections.
        multi_search (MultiSearch): Instance for performing multi-search operations.
        keys (Keys): Instance for managing API keys.
        aliases (Aliases): Instance for managing collection aliases.
        analytics (Analytics): Instance for analytics operations.
        stemming (Stemming): Instance for stemming dictionary operations.
        operations (Operations): Instance for various Typesense operations.
        debug (Debug): Instance for debug operations.
        stopwords (Stopwords): Instance for managing stopwords.
        metrics (Metrics): Instance for retrieving system and Typesense metrics.
        conversations_models (ConversationsModels): Instance for managing conversation models.
    """

    def __init__(self, config_dict: ConfigDict) -> None:
        """
        Initialize the AsyncClient instance.

        Args:
            config_dict (ConfigDict):
                A dictionary containing the configuration for the Typesense client.

        Example:
            >>> config = {
            ...     "api_key": "your_api_key",
            ...     "nodes": [
            ...         {"host": "localhost", "port": "8108", "protocol": "http"}
            ...     ],
            ...     "connection_timeout_seconds": 2,
            ... }
            >>> client = AsyncClient(config)
        """
        self.config = Configuration(config_dict)
        self.api_call = AsyncApiCall(self.config)
        self.collections: Collections[DocumentSchema] = Collections(self.api_call)
        self.multi_search = MultiSearch(self.api_call)
        self.keys = Keys(self.api_call)
        self.aliases = Aliases(self.api_call)
        self.analytics = Analytics(self.api_call)
        self.stemming = Stemming(self.api_call)
        self.operations = Operations(self.api_call)
        self.debug = Debug(self.api_call)
        self.stopwords = Stopwords(self.api_call)
        self.metrics = Metrics(self.api_call)
        self.conversations_models = ConversationsModels(self.api_call)
        self.nl_search_models = NLSearchModels(self.api_call)

    def typed_collection(
        self,
        *,
        model: typing.Type[TDoc],
        name: typing.Union[str, None] = None,
    ) -> Collection[TDoc]:
        """
        Get a Collection instance for a specific document model.

        This method allows retrieving a Collection instance typed to a specific document model.
        If no name is provided, it uses the lowercase name of the model class as
        the collection name.

        Args:
            model (Type[TDoc]): The document model class.
            name (Union[str, None], optional):
                The name of the collection. If None, uses the lowercase model class name.

        Returns:
            Collection[TDoc]: A Collection instance typed to the specified document model.

        Example:
            >>> class Company(DocumentSchema):
            ...     name: str
            ...     num_employees: int
            >>> client = AsyncClient(config)
            >>> companies_collection = client.typed_collection(model=Company)
            # This is equivalent to:
            # companies_collection = client.typed_collection(model=Company, name="company")
        """
        if name is None:
            name = model.__name__.lower()
        collection: Collection[TDoc] = self.collections[name]
        return collection
