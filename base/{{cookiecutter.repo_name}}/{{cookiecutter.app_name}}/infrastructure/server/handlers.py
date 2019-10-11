import datetime

import aiohttp_jinja2
import marshmallow as mm
import phonenumbers
from aiohttp import web

from {{cookiecutter.app_name}}.infrastructure import constants
from {{cookiecutter.app_name}}.infrastructure.call_control import CallControl
from {{cookiecutter.app_name}}.infrastructure.usecases import get_post_params
from {{cookiecutter.app_name}}.infrastructure.validators import validate_dt


@aiohttp_jinja2.template("index.html")
async def homepage(request: web.Request):
    """Renders the UI to view and schedule new calls"""

    calls_scheduler = request.app[constants.SCHEDULER]

    scheduled_calls = [
        (datetime.datetime.fromtimestamp(q_message.ts), q_message.msg)
        for q_message in calls_scheduler._queue
    ]

    date = datetime.datetime.today().strftime("%Y-%m-%d")
    time_now = datetime.datetime.now()
    time_future = time_now + datetime.timedelta(minutes=1)

    time = time_future.strftime("%H:%M")

    print(time)

    return {"scheduled_calls": scheduled_calls, "date": date, "time": time}


async def telnyx_webhook(request: web.Request) -> web.Response:
    """
    Telnyx Webhook Handler.

    Recevies the webhook from Telnyx and processes it and fires
    off the appropriate corresponding command.

    """
    call_control_app: CallControl = request.app[constants.CALL_CONTROL_APP]

    # Parse the webhook data
    data = await request.json()
    event_type = data["data"].get("event_type", "")
    call_control_id = data["data"]["payload"].get("call_control_id", None)

    # Send to the call control app to process the webhook fully
    await call_control_app.process_webhook(call_control_id, event_type)

    # Return a 200 response to the Telnyx server
    return web.Response(text="ok")


async def schedule_call(request):
    """
    POST Handler to schedule a new call
    """
    call_scheduler = request.app[constants.SCHEDULER]

    try:
        # Parse the request body
        params = await get_post_params(request)
    except Exception:
        return web.Response(
            text="Bad request. Please ensure the request is valid.", status=400
        )

    # Setup the marshmallow validators
    d = mm.fields.Date(format="%Y-%m-%d")
    t = mm.fields.Time(formt="%H:%M")

    try:
        # Validate the request
        date = d.deserialize(params["date"])
        time = t.deserialize(params["time"])
        num = phonenumbers.parse(params["phone_number"])

    except Exception:
        return web.Response(
            text="Bad request. Please ensure the request is valid.", status=400
        )

    # Create a datetime object from the request
    dt = datetime.datetime.combine(date, time)

    try:
        dt_secs = validate_dt(dt)
    except AssertionError:
        return web.Response(
            text="The scheduled time must be in the future.", status=400
        )

    call_scheduler.put(num, dt_secs)

    # Redirect the user back to the the main page
    raise web.HTTPFound("/")
