#!/usr/bin/python3
# pylint: disable=invalid-name

"""
Contains the definition for custom types

@author eLIPSE
"""

from json import dumps
from typing import Dict

# The files, a mapping of filenames to file contents
Files = Dict[str, str]

class TestResult:
    """ Stores a test result """
    exitCode: int
    stdout: str
    stderr: str

    def serialize(self):
        """ Serializes the object into a dict """
        return {
            "exitCode": self.exitCode,
            "stdout": self.stdout,
            "stderr": self.stderr
        }

    def __repr__(self):
        return dumps(self.serialize())
