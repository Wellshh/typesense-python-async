import httpx
import sys
import json
from types import MappingProxyType

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from typesense.configuration import Configuration
from typesense.exceptions import (
    HTTPStatus0Error,
    ObjectAlreadyExists,
    ObjectNotFound,
    ObjectUnprocessable,
    RequestForbidden,
    RequestMalformed,
    RequestUnauthorized,
    ServerError,
    ServiceUnavailable,
    TypesenseClientError,
)


TEntityDict = typing.TypeVar("TEntityDict")
TParams = typing.TypeVar("TParams")
TBody = typing.TypeVar("TBody")


class SessionFunctionKwargs(
    typing.Generic[TParams, TBody], typing.TypedDict, total=False
):
    """
    Type definition for keyword arguments used in async session functions.

    Attributes:
        params (Optional[Union[TParams, None]]): Query parameters for the request.

        data (Optional[Union[TBody, str, None]]): Body of the request (for form data).

        content (Optional[Union[str, bytes, None]]): Raw content of the request (for raw text/binary data).

        headers (Optional[Dict[str, str]]): Headers for the request.

        timeout (float): Timeout for the request in seconds.

        verify (bool): Whether to verify SSL certificates.
    """

    params: typing.NotRequired[typing.Union[TParams, None]]
    content: typing.NotRequired[typing.Union[str, bytes, None]]
    headers: typing.NotRequired[typing.Dict[str, str]]
    timeout: float
    verify: bool


_ERROR_CODE_MAP: typing.Mapping[str, typing.Type[TypesenseClientError]] = (
    MappingProxyType(
        {
            "0": HTTPStatus0Error,
            "400": RequestMalformed,
            "401": RequestUnauthorized,
            "403": RequestForbidden,
            "404": ObjectNotFound,
            "409": ObjectAlreadyExists,
            "422": ObjectUnprocessable,
            "500": ServerError,
            "503": ServiceUnavailable,
        },
    )
)


class AsyncRequestHandler:
    """
    Handles asynchronous HTTP requests to the Typesense API.

    This is the asynchronous version of the RequestHandler class.
    This class manages authentication, request sending, and response processing
    for interactions with the Typesense API.

    Attributes:
        api_key_header_name (str): The header name for the API key.
        config (Configuration): The configuration object for the Typesense client.
    """

    api_key_header_name: typing.Final[str] = "X-TYPESENSE-API-KEY"

    def __init__(self, config: Configuration):
        self.config = config

    @typing.overload
    async def make_request(
        self,
        fn: typing.Callable[..., httpx.Response],
        url: str,
        entity_type: typing.Type[TEntityDict],
        as_json: typing.Literal[False],
        **kwargs: typing.Unpack[SessionFunctionKwargs[TParams, TBody]],
    ) -> str:
        """
        Make an asynchronous HTTP request to the Typesense API and return the response as a string.

        This overload is used when as_json is set to False, indicating that the response
        should be returned as a raw string instead of being parsed as JSON.

        Args:
            fn (Callable): The asynchronous HTTP method function to use (e.g., httpx.get).

            url (str): The URL to send the request to.

            entity_type (Type[TEntityDict]): The expected type of the response entity.

            as_json (Literal[False]): Specifies that the response should not be parsed as JSON.

            kwargs: Additional keyword arguments for the request.

        Returns:
            str: The raw string response from the API.

        Raises:
            TypesenseClientError: If the API returns an error response.
        """

    @typing.overload
    async def make_request(
        self,
        fn: typing.Callable[..., httpx.Response],
        url: str,
        entity_type: typing.Type[TEntityDict],
        as_json: typing.Literal[True],
        **kwargs: typing.Unpack[SessionFunctionKwargs[TParams, TBody]],
    ) -> TEntityDict:
        """
        Make an asynchronous HTTP request to the Typesense API.

        Args:
            fn (Callable): The asynchronous HTTP method function to use (e.g., httpx.get).

            url (str): The URL to send the request to.

            entity_type (Type[TEntityDict]): The expected type of the response entity.

            as_json (bool): Whether to return the response as JSON. Defaults to True.

            kwargs: Additional keyword arguments for the request.

        Returns:
            TEntityDict: The response, as a JSON object.

        Raises:
            TypesenseClientError: If the API returns an error response.
        """

    async def make_request(
        self,
        fn: typing.Callable[..., httpx.Response],
        url: str,
        entity_type: typing.Type[TEntityDict],
        as_json: typing.Union[typing.Literal[True], typing.Literal[False]] = True,
        **kwargs: typing.Unpack[SessionFunctionKwargs[TParams, TBody]],
    ) -> typing.Union[TEntityDict, str]:
        """
        Make an asynchronous HTTP request to the Typesense API.

        Args:
            fn (Callable): The asynchronous HTTP method function to use (e.g., httpx.AsyncClient.get).

            url (str): The URL to send the request to.

            entity_type (Type[TEntityDict]): The expected type of the response entity.

            as_json (bool): Whether to return the response as JSON. Defaults to True.

            kwargs: Additional keyword arguments for the httpxrequest.

        Returns:
            Union[TEntityDict, str]: The response, either as a JSON object or a string.

        Raises:
            TypesenseClientError: If the API returns an error response.
        """
        headers = {
            self.api_key_header_name: self.config.api_key,
        }
        headers.update(self.config.additional_headers)

        kwargs.setdefault("headers", {}).update(headers)
        kwargs.setdefault("timeout", self.config.connection_timeout_seconds)
        if kwargs.get("content") and not isinstance(kwargs["content"], (str, bytes)):
            kwargs["content"] = json.dumps(kwargs["content"])

        response = await fn(url, **kwargs)

        if response.status_code < 200 or response.status_code >= 300:
            error_message = self._get_error_message(response)
            raise self._get_exception(response.status_code)(
                response.status_code,
                error_message,
            )

        if as_json:
            res: TEntityDict = response.json()
            return res

        return response.text

    @staticmethod
    def normalize_params(params: TParams) -> None:
        """
        Normalize boolean parameters in the request.

        Args:
            params (TParams): The parameters to normalize.

        Raises:
            ValueError: If params is not a dictionary.
        """
        if not isinstance(params, typing.Dict):
            raise ValueError("Params must be a dictionary.")
        for key, parameter_value in params.items():
            if isinstance(parameter_value, bool):
                params[key] = str(parameter_value).lower()

    @staticmethod
    def _get_error_message(response: httpx.Response) -> str:
        """
        Extract the error message from an API response.

        Args:
            response (httpx.Response): The API response.

        Returns:
            str: The extracted error message or a default message.
        """
        content_type = response.headers.get("Content-Type", "")
        if content_type.startswith("application/json"):
            try:
                return typing.cast(str, response.json().get("message", "API error."))
            except json.JSONDecodeError or UnicodeDecodeError:  # noqa: B030
                return f"API error: Invalid JSON response: {response.text}"
        return "API error."

    @staticmethod
    def _get_exception(http_code: int) -> typing.Type[TypesenseClientError]:
        """
        Map an HTTP status code to the appropriate exception type.

        Args:
            http_code (int): The HTTP status code.

        Returns:
            Type[TypesenseClientError]: The exception type corresponding to the status code.
        """
        return _ERROR_CODE_MAP.get(str(http_code), TypesenseClientError)
