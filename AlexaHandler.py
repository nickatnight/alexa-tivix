import json
import urllib2

from bs4 import BeautifulSoup
from pyalexaskill.AlexaBaseHandler import AlexaBaseHandler

from utilities.utils import IntentHandler


class AlexaTivixHandler(AlexaBaseHandler):

    # Sample concrete implementation of the AlexaBaseHandler to test the
    # deployment scripts and process.
    # All on_ handlers call the same test response changing the request type
    # spoken.


    def __init__(self, app_id=None):
        super(self.__class__, self).__init__(app_id)


    def _test_response(self, msg):
        session_attributes = {}
        card_title = "Test Response"
        card_output = "Test card output"
        speech_output = "Welcome to the Python Alexa Test Deployment for request type {0}.  It seems to have worked".format(
            msg)
        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
        reprompt_text = "Reprompt text for the Alexa Test Deployment"
        should_end_session = True

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text,
                                                   should_end_session)

        return self._build_response(session_attributes, speechlet)


    def on_processing_error(self, event, context, exc):
        session_attributes = {}
        card_title = "Error"
        speech_output = "I am having difficulty fulfilling your request."

        reprompt_text = "I did not hear you"
        should_end_session = True

        if exc:
            speech_output = "I am having difficulty fulfilling your request. {0}".format(exc.message)

        card_output = speech_output
        speechlet = self._build_speechlet_response(card_title,
                                                   card_output,
                                                   speech_output,
                                                   reprompt_text,
                                                   should_end_session)

        return self._build_response(session_attributes, speechlet)


    def on_launchrequest(self, launch_request, session):
        session_attributes = {}
        card_title = "Welcome"
        card_output = "Welcome to the Tivix Alexa App"
        speech_output = "Welcome to the Tivix Alexa App. How may we innovate engineering for you today?"

        reprompt_text = "I'm afraid I did not hear you"
        should_end_session = False
        speechlet = self._build_speechlet_response(card_title,
                                                   card_output,
                                                   speech_output,
                                                   reprompt_text,
                                                   should_end_session)

        return self._build_response(session_attributes, speechlet)


    def on_session_started(self, session_started_request, session):
        return self._test_response("on session started")


    def on_intent(self, intent_request, session):
        response = None
        session_attributes = {}
        reprompt_text = "I'm afraid I did not hear you"
        should_end_session = False

        intent_name = self._get_intent_name(intent_request)

        slot_packet = self.assemble_slot_packets(intent_request)

        intent_handler = IntentHandler(slot_packet, intent_request, session)

        # get the speech output
        speech_packet= intent_handler.run_handler(intent_name)
        speechlet = self._build_speechlet_response(
            speech_packet['card_title'],
            speech_packet['card_output'],
            speech_packet['speech_output'],
            speech_packet['reprompt_text'],
            speech_packet['should_end_session']
        )

        response = self._build_response(session_attributes, speechlet)

        # else:
        #     raise ValueError("Invalid intent")

        return response

    def on_session_ended(self, session_end_request, session):
        return self._test_response("on session end")

    def on_help_intent(self, intent_request, session):
        session_attributes = {}
        card_output = "Card Help"
        speech_output = "Speech Help"

        reprompt_text = "I did not hear you, {0}".format(speech_output)
        should_end_session = False
        speechlet = self._build_speechlet_response(self.card_title,
                                                   card_output,
                                                   speech_output,
                                                   reprompt_text,
                                                   should_end_session)

        return self._build_response(session_attributes, speechlet)

    def on_stop_intent(self, intent_request, session):
        return self.on_cancel_intent(intent_request, session)

    def on_cancel_intent(self, intent_request, session):
        session_attributes = {}
        card_output = "Thank you and Good-bye"
        speech_output = "Thank you and Good-bye"

        reprompt_text = "{0}".format(speech_output)
        should_end_session = True
        speechlet = self._build_speechlet_response(self.card_title,
                                                   card_output,
                                                   speech_output,
                                                   reprompt_text,
                                                   should_end_session)

        return self._build_response(session_attributes, speechlet)

    def on_no_intent(self, intent_request, session):
        return self._test_response("on no intent")

    def on_yes_intent(self, intent_request, session):
        return self._test_response("on yes intent")

    def on_repeat_intent(self, intent_request, session):
        return self._test_response("on repeat intent")

    def on_startover_intent(self, intent_request, session):
        return self._test_response("on start over intent")

    def assemble_slot_packets(self, intent_request):
        slots = {}

        with open('assets/IntentSchema.json') as data_file:
            data = json.load(data_file)

        for intent in data['intents']:
            if 'slots' in intent:
                for slot in intent['slots']:
                    slot_name = slot['name']
                    value = 'None'
                    exists = self._slot_exists(slot_name, intent_request)

                    if exists:
                        value = self._get_slot_value(slot_name, intent_request)

                    slots[slot_name] = { 'exists': exists, 'value': value }

        return slots
