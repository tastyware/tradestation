from typing import Any
from httpx._models import Response
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


class TradestationError(Exception):
    """
    An internal error raised by the Tradestation SDK.
    """

    pass


class TradestationModel(BaseModel):
    """
    A pydantic dataclass that converts keys from snake case to Pascal case
    and performs type validation and coercion.
    """

    model_config = ConfigDict(alias_generator=to_pascal, populate_by_name=True)


def validate_response(response: Response) -> None:
    """
    Checks if the given code is an error; if so, raises an exception.

    :param response: response to check for errors
    """
    if response.status_code // 100 != 2:
        data = response.json()
        if "error" in data:
            raise TradestationError(f"{data['error']}: {data['error_description']}")
        else:
            raise TradestationError(f"{data['Error']}: {data['Message']}")


def validate_and_parse(response: Response) -> Any:
    """
    Validates a response, then returns its content as parsed JSON.
    """
    validate_response(response)
    return response.json()
