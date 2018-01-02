"""
The REST api server for the coderunner

@author eLIPSE
"""

from flask import Flask, request
from json import dumps
from typing import Dict
from codesandbox.sandbox import run_code, run_gui_code

app = Flask(__name__)

def validate_request(request: Dict) -> bool:
    """ Validates the user's request """

    assert request is not None, "no JSON payload"

    # Check that the files are there
    assert "files" in request, "no 'files' field in payload"

    # Check that the gui flag is there
    assert "isGui" in request, "no 'isGui' field in payload"

def generate_error_response(message: str) -> Dict:
    """ Generates an error message to send over the send over the API

    Will send it with a 400 status code
    """

    return dumps({
        "msg": message
    }), 400



@app.route("/run", methods=["POST"])
def run():
    """
    The payload should take the form of:

        {
            "files": {
                "test.py": "print('Hello world')"
            },
            isGui: false
        }
    """
    try:
        is_valid = validate_request(request.get_json())
    except AssertionError as e:
        return generate_error_response(str(e))


    req = request.get_json()
    files = req["files"]
    isGui = req["isGui"]

    if isGui:
        return dumps(run_gui_code(files).serialize())
    else:
        return dumps(run_code(files).serialize())

