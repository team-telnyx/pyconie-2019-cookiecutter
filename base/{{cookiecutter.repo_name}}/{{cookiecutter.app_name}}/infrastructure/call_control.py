"""
The call control app
Processes webhooks and controls the flow of active calls
"""

import asyncio
from typing import Mapping, Optional

import phonenumbers
import telnyx
from aiohttp import ClientSession


class CallControl:
    """
    This class handles all incoming telnyx call control webhooks.

    Creates the initial call request, and handles all subsequent webhooks.
    """

    def __init__(
        self,
        client_session: ClientSession,
        telnyx_app: telnyx,
        connection_id: str,
        joke_url: str,
        src_number: str,
    ) -> None:
        self._client_session = client_session
        self._telnyx_app = telnyx_app
        self._connection_id = connection_id
        self._joke_url = joke_url
        self._src_number = src_number

    async def _get_joke(self) -> str:
        """Calls out to the joke API and parses the response
        and returns the given joke as a string.
        """
        headers = {"Accept": "application/json"}

        # Make the GET request to the Joke API
        resp = await self._client_session.get(self._joke_url, headers=headers)

        # Parse the json from the response
        joke = await resp.json()

        # Return the joke
        return joke["joke"]

    async def process_webhook(
        self, call_control_id: Optional[str], event_type: str
    ) -> None:
        """
        Processes the incoming webhook depending on the event type.

        Checks the event type in the webhook and follows the sequence for that event.

        For call.answered, get the joke and speak the joke.

        For call.speak.ended, hang up the call.
        """
        # Create the call object and populate it with the webhook call control id
        current_call = self._telnyx_app.Call()
        current_call.call_control_id = call_control_id

        if event_type == "call.answered":
            # Get the joke
            jk = await self._get_joke()

            # Sleep to ensure the speak happens after the user is listening
            await asyncio.sleep(0.5)

            # Request the joke be spoken in the call
            current_call.speak(payload=jk, voice="male", language="en-GB")

            return

        if event_type == "call.speak.ended":
            # Hang up the call after the joke is finished
            current_call.hangup()

    async def dial(self, data) -> None:
        """This takes in call data and initates the call.
        Saves the information to self._requested_calsl to be tracked with future webhooks.

        """
        # Format the number in +E.164 format
        dst = phonenumbers.format_number(data, phonenumbers.PhoneNumberFormat.E164)

        # Request the call to be initiated
        self._telnyx_app.Call.create(
            connection_id=self._connection_id, to=dst, from_=self._src_number
        )
