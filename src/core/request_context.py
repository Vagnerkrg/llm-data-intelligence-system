"""
Request context management.

Provides request identification
across application execution flow.
"""


from contextvars import ContextVar
from uuid import uuid4



_request_id_context: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None
)



def create_request_id() -> str:
    """
    Creates a unique request identifier.
    """

    return str(
        uuid4()
    )



def set_request_id(
    request_id: str | None = None
) -> str:
    """
    Stores request id in current execution context.

    If no id is provided, a new one is generated.
    """


    if request_id is None:

        request_id = create_request_id()



    _request_id_context.set(
        request_id
    )


    return request_id



def get_request_id() -> str:
    """
    Returns current request identifier.
    """

    request_id = _request_id_context.get()



    if request_id is None:

        request_id = set_request_id()



    return request_id



def clear_request_id():
    """
    Clears current request context.
    """

    _request_id_context.set(
        None
    )