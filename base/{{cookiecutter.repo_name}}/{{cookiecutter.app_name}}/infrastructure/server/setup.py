"""
Setup functions for HTTP server.
"""

import aiohttp_cors

from {{cookiecutter.app_name}}.infrastructure.server import handlers, health_handlers


# Define the private diagnostic paths
HEALTH = "/health"
INFO = "/info"

# Define the public paths
HOME = "/"
TELNYX_WEBHOOK = "/webhook"


def _setup_routes(app):
    """Add routes to the given aiohttp app."""

    # Default cors settings.
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )

    # App Health check.
    app.router.add_get(HEALTH, health_handlers.health_check)

    # App Metadata.
    app.router.add_get(INFO, health_handlers.info)

    # Webhoook Routes.
    cors.add(app.router.add_post(TELNYX_WEBHOOK, handlers.telnyx_webhook))

    # Schedule Calls.
    cors.add(app.router.add_get(HOME, handlers.homepage))
    cors.add(app.router.add_post(HOME, handlers.schedule_call))


def _setup_middlewares(app):
    """Add middlewares to the given aiohttp app."""
    pass


def configure_app(app, startup_handler):
    """Configure the web.Application."""

    _setup_routes(app)
    _setup_middlewares(app)

    # Schedule custom startup routine.
    app.on_startup.append(startup_handler)
