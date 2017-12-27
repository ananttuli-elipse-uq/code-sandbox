"""
Tests the sandbox module
"""

from unittest import TestCase, main
from sandbox import run_code

class TestSandbox(TestCase):
    """ Test the sandbox code execution """

    def test_basic(self):
        """ Tests basic code running """
        files = {
            "test.py": "print('Hello world')",
        }

        output = {
            "stdout": "Hello world\n",
            "stderr": "",
            "exitCode": 0
        }

        result = run_code(files)

        self.assertEqual(result.serialize(), output)

    def test_import(self):
        """ Tests importing other modules """
        files = {
            "test.py": "import file2\nprint('Hello world')",
            "file2.py": "print('File2')",
        }

        output = {
            "stdout": "File2\nHello world\n",
            "stderr": "",
            "exitCode": 0
        }

        result = run_code(files)

        self.assertEqual(result.serialize(), output)


if __name__ == "__main__":
    main()
