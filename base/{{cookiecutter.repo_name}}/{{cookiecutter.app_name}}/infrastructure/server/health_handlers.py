"""
HTTP health check.
"""

import datetime
import json
import os
import socket
import time

from aiohttp import web

START_TIME = time.time()

INFO = {"host": socket.gethostname()}


def _dumps(obj):
    """Pretty JSON"""
    return json.dumps(obj, indent=4, sort_keys=True) + "\n"


async def health_check(_request: web.Request):
    """Health check handler."""
    return web.json_response({"status": "OK"})


async def info(_request: web.Request):
    """Metadata."""
    INFO["start_time"] = str(round(START_TIME, 2))
    INFO["uptime"] = f"{round(time.time() - START_TIME, 2)} s"
    INFO["date"] = datetime.datetime.now().isoformat()
    return web.json_response(INFO, dumps=_dumps)
