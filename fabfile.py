from fabric.api import *
from fabric.colors import red
from fabric.contrib.console import confirm
from fabric.operations import prompt
import platform


# Give beautiful display of errors
env.colorize_errors = True

# Files intended to get zipped for AWS lambda file upload
FILES = [
    'AlexaHandler.py',
    'main.py',
    'assets/IntentSchema.json',
    'utilities/__init__.py',
    'utilities/utils.py',
    'utilities/consts.py'
]

def zip_files():
    """Create .zip for lambda

    https://github.com/youngsoul/PyAlexa#create_aws_lambdapy
    """
    file_list = ', '.join(FILES)
    local('create_aws_lambda.py -i "' + file_list + '"')
