"""
Tests the sandbox module
"""

from unittest import TestCase, main
from codesandbox.sandbox import run_code, run_gui_code

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
            "exitCode": 0,
            "img": None
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
            "exitCode": 0,
            "img": None
        }

        result = run_code(files)

        self.assertEqual(result.serialize(), output)

    def test_infinite_loop(self):
        """ Tests that infinite loops are terminated """
        files = {
            "test.py": "while 1:\n\tprint('test')"
        }

        output = {
            "stdout": "",
            "stderr": "Code did not finish, possible infinite loop",
            "exitCode": 1,
            "img": None
        }


class TestGuiSandbox(TestCase):
    """ Tests GUI sandboxing """

    def test_simple_gui(self):
        """ Tests importing other modules """

        script_contents = ""
        with open("./codesandbox/test_scripts/sample_gui.py", "r") as script:
            script_contents = script.read()

        files = {
            "test.py": script_contents,
        }

        img_data = ""
        with open("./codesandbox/test_scripts/sample_gui_img_out", "r") as img:
            img_data = img.read().strip()

        result = run_gui_code(files)

        # Check to see if it produces the correct image
        self.assertEqual(result.img, img_data)


if __name__ == "__main__":
    main()
