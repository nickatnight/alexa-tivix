import urllib2

from bs4 import BeautifulSoup

from utilities.consts import TIVIX_URLS


class IntentHandler(object):
    def __init__(self, slot_packet, intent_request, session):
        self.slot_packet = slot_packet
        self.intent_request = intent_request
        self.session = session
        self.erros = {}

    def get_page_content(self, page_url):
        request = urllib2.urlopen(page_url)
        soup = BeautifulSoup(request, 'html.parser')

        return soup

    def run_handler(self, intent):
        speech_packet = {}
        if intent == "TeamIntent":
            speech_packet = self.team_intent()
        elif intent == "WhichEmployeeIntent":
            speech_packet = self.which_employee_intent()
        elif intent == "WhoAreWeIntent":
            speech_packet = self.who_we_are()
        elif intent == "WhatWeDoIntent":
            speech_packet = self.what_we_do()
        else:
            raise ValueError("Invalid intent")

        return speech_packet

    def team_intent(self):
        soup = self.get_page_content(TIVIX_URLS['team'])
        members = soup.findAll('div', attrs={'class': 'team-overlay'})
        employee_total = str(len(members))
        speech_output = "There are currently %s ridiculously smart and passionate individuals who work at Tivix. Would you like to know about a particular employee?" % (employee_total, )

        packet = Packet(
            False,
            "Team Info",
            "Info on team members",
            "I'm afraid I did not hear you",
            speech_output
        )

        return packet.deliver()

    def which_employee_intent(self):
        speech_output = "This did not work"
        soup = self.get_page_content(TIVIX_URLS['team'])
        first_name, last_name = None, None

        members = soup.findAll('div', attrs={'class': 'team-overlay'})

        if self.slot_packet['EmployeeFirstName']['exists'] and self.slot_packet['EmployeeLastName']['exists']:
            first_name = self.slot_packet['EmployeeFirstName']['value'].lower()
            last_name = self.slot_packet['EmployeeLastName']['value'].lower()

            for member in members:
                name = member.contents[0].text.lower() + ' ' + member.contents[2].text.lower()
                if name == "%s %s" % (first_name, last_name):

                    employee_page = "%s%s-%s/" % (TIVIX_URLS['team'], first_name, last_name)
                    soup = self.get_page_content(employee_page)
                    speech_output = soup.find('div', attrs={'class': 'rich-text'}).text

        # elif self._slot_exists("EmployeeFirstName", self.intent_request):
        #     first_name = self._get_slot_value("EmployeeFirstName", self.intent_request)
        #
        #     for member in members:
        #         if member.contents[0].split(' ')[0].lower() == first_name:
        #             speech_output = "This worked"


        packet = Packet(
            True,
            "Employee Info",
            "Info on team members",
            "I'm afraid I did not hear that name",
            speech_output
        )

        return packet.deliver()

    def who_we_are(self):
        soup = self.get_page_content(TIVIX_URLS['services'])
        who_we_are_text = soup.find('div', attrs={'class': 'text-container position-center valign-middle justify-left'}).find('div', attrs={'class': 'rich-text'}).text
        speech_output = "Well that's a really good question. We are a bunch of things, but mainly, %s" % (who_we_are_text, )
        packet = Packet(
            True,
            "Who we are",
            "Info on us",
            "I'm afraid I did not hear that name",
            speech_output
        )

        return packet.deliver()

    def what_we_do(self):
        soup = self.get_page_content(TIVIX_URLS['services'])
        msg = soup.find('div', attrs={'class': 'rich-text'}).text
        packet = Packet(
            True,
            "What we do",
            "More info on us",
            "I'm afraid I did not catch that",
            msg
        )

        return packet.deliver()

class Packet(object):
    def __init__(self, session_end, card_title, card_output, reprompt_text, speech_output):
        self.session_end = session_end
        self.card_title = card_title
        self.card_output = card_output
        self.reprompt_text = reprompt_text
        self.speech_output = speech_output

    def deliver(self):
        delivery = {
            'should_end_session': self.session_end,
            'card_title': self.card_title,
            'card_output': self.card_output,
            'reprompt_text': self.reprompt_text,
            'speech_output': self.speech_output
        }

        return delivery
