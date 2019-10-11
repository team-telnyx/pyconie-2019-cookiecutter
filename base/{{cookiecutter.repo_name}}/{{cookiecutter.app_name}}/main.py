"""
{{cookiecutter.app_name}}

{{cookiecutter.project_short_description}}
"""
import asyncio
import json
import logging
import os
import signal
import socket
import sys
from pathlib import Path
from typing import Mapping

import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2
import telnyx

from {{cookiecutter.app_name}}.infrastructure import constants
from {{cookiecutter.app_name}}.infrastructure import server
from {{cookiecutter.app_name}}.infrastructure.call_control import CallControl
from {{cookiecutter.app_name}}.infrastructure.scheduler import UnifiedTimedQueue


def on_startup(conf: Mapping):
    """Return a startup handler that will bootstrap and then begin background tasks."""

    async def startup_handler(app):
        """Run all initialization tasks.

        These are tasks that should be run after the event loop has been started but before the HTTP
        server has been started.
        """
        # Pull configurations
        joke_url = conf["jokes_external_api_url"]
        telnyx_api_key = conf["telnyx_api_key"]
        telnyx_connection_id = conf["telnyx_connection_id"]
        src_number = conf["src_number"]

        # Setup client session
        client_session = aiohttp.ClientSession()

        # Setup Telnyx settings
        telnyx.api_key = telnyx_api_key

        # Setup the jinga template for the front-end webpage
        templates_dir = Path(conf["templates_dir"]).resolve()
        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(templates_dir)))

        # Setup the Call Control App
        call_control_app = CallControl(
            client_session, telnyx, telnyx_connection_id, joke_url, src_number
        )

        # Setup the Call Schedule
        call_scheduler = UnifiedTimedQueue(call_control_app)

        # Register App dependencies
        # These will be accessible via the Request object
        app[constants.SCHEDULER] = call_scheduler
        app[constants.TELNYX] = telnyx
        app[constants.CALL_CONTROL_APP] = call_control_app

        # Define required cleanup
        async def cleanup(app):
            """Perform required cleanup on shutdown"""
            await client_session.close()

        app.on_shutdown.append(cleanup)

    return startup_handler


def main():
    # Load config.
    with open("config.dev.json", "r") as f:
        conf = json.load(f)

    # Set some runtime variables.
    hostname = os.environ.get("SERVER_HOSTNAME", socket.gethostname()).split(".", 1)[0]
    conf["runtime"] = {"app_name": "dial-a-joke", "hostname": hostname}

    # Initialize logger.
    logging.basicConfig(stream=sys.stdout, level="INFO")

    http_socket = conf["http"]

    # Setup the web server.
    app = web.Application()

    # Configure the web server.
    server.configure_app(app, on_startup(conf))

    # Start the HTTP server.
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, loop.stop)
    web.run_app(app, host=http_socket["host"], port=http_socket["port"])


if __name__ == "__main__":
    sys.exit(main())
