import json
from typing import Mapping

from aiohttp import web


async def get_post_params(request: web.Request) -> Mapping:
    """Get POST parameters from the request.

    Accept either application/x-www-form-urlencoded or application/json.

    Returns: A mapping of the params.
    """

    if request.content_type == "application/x-www-form-urlencoded":
        params = await request.post()

    elif request.content_type == "application/json":
        try:
            params = await request.json()
        except Exception as e:
            raise e
    else:
        raise TypeError

    return params
