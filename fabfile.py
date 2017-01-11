from fabric.api import *
from fabric.colors import red
from fabric.contrib.console import confirm
from fabric.operations import prompt
import platform


# Give beautiful display of errors
env.colorize_errors = True


def lambda_push():
    local('create_aws_lambda.py -i "AlexaHandler.py, main.py, utilities/__init__.py, utilities/consts.py"')
