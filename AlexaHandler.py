import urllib2

from bs4 import BeautifulSoup
from pyalexaskill.AlexaBaseHandler import AlexaBaseHandler

from utilities.consts import TIVIX_URLS


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

        if intent_name == "TeamIntent":
            page = TIVIX_URLS['team']

            r = urllib2.urlopen(page)

            soup = BeautifulSoup(r, 'html.parser')

            members = soup.findAll('div', attrs={'class': 'team-overlay'})

            employee_total = str(len(members))

            card_title = "Team Info"
            card_output = "Info on team members"
            speech_output = "There are currently %s ridiculously smart and passionate individuals who work at Tivix. Together we've helped organizations across many sectors to build innovative software that has improved their ability to create value and deliver impact. Would you like to know about a particular employee?" % (employee_total, )
            speechlet = self._build_speechlet_response(card_title,
                                                       card_output,
                                                       speech_output,
                                                       reprompt_text,
                                                       should_end_session)

            response = self._build_response(session_attributes, speechlet)

        elif intent_name == "WhichEmployeeIntent":
            page = TIVIX_URLS['team']
            first_name = None
            last_name = None
            speech_output = "This didn't work"
            r = urllib2.urlopen(page)
            should_end_session = True

            soup = BeautifulSoup(r, 'html.parser')

            members = soup.findAll('div', attrs={'class': 'team-overlay'})

            if self._slot_exists("EmployeeFirstName", intent_request) and self._slot_exists("EmployeeLastName", intent_request):
                first_name = self._get_slot_value("EmployeeFirstName", intent_request).lower()
                last_name = self._get_slot_value("EmployeeLastName", intent_request).lower()

                for member in members:
                    if member.contents[0].lower() == "%s %s" % (first_name, last_name):

                        employee_page = "%s%s-%s/" % (page, first_name, last_name)
                        r = urllib2.urlopen(employee_page)
                        soup = BeautifulSoup(r, 'html.parser')
                        speech_output = soup.find('div', attrs={'class': 'rich-text'}).text

            elif self._slot_exists("EmployeeFirstName", intent_request):
                first_name = self._get_slot_value("EmployeeFirstName", intent_request)

                for member in members:
                    if member.contents[0].split(' ')[0].lower() == first_name:
                        speech_output = "This worked"

            card_title = "Employee Info"
            card_output = "Info on team members"
            speechlet = self._build_speechlet_response(card_title,
                                                       card_output,
                                                       speech_output,
                                                       reprompt_text,
                                                       should_end_session)

            response = self._build_response(session_attributes, speechlet)

        else:
            raise ValueError("Invalid intent")

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
