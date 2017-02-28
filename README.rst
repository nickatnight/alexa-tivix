
|Alexa| <-> |Tivix|

.. |Alexa| image:: images/amazon-alexa.png
.. |Tivix| image:: images/tivix.png

==================================================================
Alexa-Tivix: Tivix Application for Alexa powered devices
==================================================================


To run, ``fab lambda_push`` in venv to create zip file to upload to AWS lambda.

This application was built with PyPi package: ``pyalexa-skill``

Github link: https://github.com/youngsoul/PyAlexa

requirements.txt
----------------
For some reason, I'm getting errors when I try to upload zip file to AWS lambda
that includes a requirements file with Fabric packages, so for now, I am omitting those.


Usage
-----

*Ask Tivix*

- Alexa will greet you with a brief introduction of the company. (The session will still be open, so at this point, there are several utterances you can proceed with)

*What does Tivix do?*

*What do they do?*

- Alexa will provide a brief description of the company and goals.

*How many people work at tivix?*

*How many people work there?*

*Who works there?*

*How many employees work there?*

- Alexa will dynamically get the total number of employees by scrapping tivix.com/team-members/ and utter the total amount, and then proceed by asking if you would like more info on a particular employee. Currently, you must provide a first AND last name (There are multiple employees with the same first name). Once determined, Alexa will read that chosen employees bio off Tivix.com

*Who is Tivix?*

*Who they are?*

*Who are they?*

- blah blah blah

*What is Tivix?*

*What is it?*

*What is a Tivix?*

*What does Tivix mean?*

- blah blah blah

http://www.tivix.com
