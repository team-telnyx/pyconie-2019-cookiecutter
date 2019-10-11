import asyncio
import json
import os
from unittest.mock import Mock

from aiohttp import web
from aiohttp.test_utils import TestServer
import pytest

import telnyx

from {{cookiecutter.app_name}}.infrastructure import constants
from {{cookiecutter.app_name}}.infrastructure import server


@pytest.fixture
def web_app(loop):
    async def startup_handler(app):
        # Save dependencies in the HTTP app.

        # Mock the telnyx SDK
        telnyx = Mock()
        telnyx.Call().return_value = Mock()

        app[constants.TELNYX] = telnyx

    # Create the test web application
    app = web.Application()

    # Configure the test web app with the same configurations
    server.configure_app(app, startup_handler)
    return app


@pytest.fixture
async def test_client(aiohttp_client, web_app):
    """Create a test client with mocked endpoints"""
    return await aiohttp_client(web_app)
