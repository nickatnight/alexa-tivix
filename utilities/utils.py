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

        return speech_packet

    def team_intent(self):
        packet = {}
        soup = self.get_page_content(TIVIX_URLS['team'])
        packet['should_end_session'] = False
        packet['card_title'] = "Team Info"
        packet['card_output'] = "Info on team members"
        packet['reprompt_text'] = "I'm afraid I did not hear you"

        members = soup.findAll('div', attrs={'class': 'team-overlay'})

        employee_total = str(len(members))

        packet['speech_output'] = "There are currently %s ridiculously smart and passionate individuals who work at Tivix. Together we've helped organizations across many sectors to build innovative software that has improved their ability to create value and deliver impact. Would you like to know about a particular employee?" % (employee_total, )
        return packet

    def which_employee_intent(self):
        packet = {}
        soup = self.get_page_content(TIVIX_URLS['team'])
        speech_output = "This didn't work"
        first_name, last_name = None, None
        packet['should_end_session'] = True
        packet['card_title'] = "Employee Info"
        packet['card_output'] = "Info on team members"
        packet['reprompt_text'] = "I'm afraid I did not hear that name"

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

        packet['speech_output'] = speech_output

        return packet
