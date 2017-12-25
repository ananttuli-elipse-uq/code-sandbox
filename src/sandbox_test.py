"""
Tests the sandbox module
"""

from unittest import TestCase, main
from sandbox import run_code

class TestSandbox(TestCase):

    def test_basic(self):
        """ Tests basic code running """
        FILES = {
            "test.py": "print('Hello world')",
        }

        output = {
            "stdout": "Hello world\n",
            "stderr": "",
            "exitCode": 0
        }

        result = run_code(FILES)

        self.assertEqual(result.serialize(), output)

    def test_import(self):
        """ Tests importing other modules """
        FILES = {
            "test.py": "import file2\nprint('Hello world')",
            "file2.py": "print('File2')",
        }

        output = {
            "stdout": "File2\nHello world\n",
            "stderr": "",
            "exitCode": 0
        }

        result = run_code(FILES)

        self.assertEqual(result.serialize(), output)


if __name__ == "__main__":
    main()
