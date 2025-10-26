"""
This module provides functionality for asynchronously managing NL search models in Typesense.

Classes:
    - NLSearchModels: Handles operations related to NL search models.

Methods:
    - __init__: Initializes the NLSearchModels object.
    - __getitem__: Retrieves or creates an NLSearchModel object for a given model_id.
    - create: Creates a new NL search model.
    - retrieve: Retrieves all NL search models.

Attributes:
    - resource_path: The API resource path for NL search models operations.

The NLSearchModels class interacts with the Typesense API to manage
NL search model operations.

It provides methods to create and retrieve NL search models, as well as access
individual NLSearchModel objects.

This module uses type hinting and is compatible with Python 3.11+ as well as earlier
versions through the use of the typing_extensions library.
"""

import sys

from typesense.async_client.async_api_call import AsyncApiCall
from typesense.types.nl_search_model import (
    NLSearchModelCreateSchema,
    NLSearchModelSchema,
    NLSearchModelsRetrieveSchema,
)

if sys.version_info > (3, 11):
    import typing
else:
    import typing_extensions as typing

from typesense.async_client.nl_search_model import NLSearchModel


class NLSearchModels(object):
    """
    Class for managing NL search models in Typesense.

    This class provides methods to interact with NL search models, including
    creating, retrieving, and accessing individual models.

    Attributes:
        resource_path (str): The API resource path for NL search models operations.
        api_call (AsyncApiCall): The AsyncApiCall object for making requests.
        nl_search_models (Dict[str, NLSearchModel]):
            A dictionary of NLSearchModel objects.
    """

    resource_path: typing.Final[str] = "/nl_search_models"

    def __init__(self, api_call: AsyncApiCall) -> None:
        """
        Initialize the NLSearchModels object.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall object for making requests.
        """
        self.api_call = api_call
        self.nl_search_models: typing.Dict[str, NLSearchModel] = {}

    def __getitem__(self, model_id: str) -> NLSearchModel:
        """
        Get or create an NLSearchModel object for a given model_id.

        Args:
            model_id (str): The ID of the NL search model.

        Returns:
            NLSearchModel: The NLSearchModel object for the given ID.
        """
        if model_id not in self.nl_search_models:
            self.nl_search_models[model_id] = NLSearchModel(
                self.api_call,
                model_id,
            )
        return self.nl_search_models[model_id]

    async def create(self, model: NLSearchModelCreateSchema) -> NLSearchModelSchema:
        """
        Create a new NL search model.

        Args:
            model (NLSearchModelCreateSchema):
                The schema for creating the NL search model.

        Returns:
            NLSearchModelSchema: The created NL search model.
        """
        response = await self.api_call.post(
            endpoint=NLSearchModels.resource_path,
            entity_type=NLSearchModelSchema,
            as_json=True,
            body=model,
        )
        return response

    async def retrieve(self) -> NLSearchModelsRetrieveSchema:
        """
        Retrieve all NL search models.

        Returns:
            NLSearchModelsRetrieveSchema: A list of all NL search models.
        """
        response: NLSearchModelsRetrieveSchema = await self.api_call.get(
            endpoint=NLSearchModels.resource_path,
            entity_type=NLSearchModelsRetrieveSchema,
            as_json=True,
        )
        return response
