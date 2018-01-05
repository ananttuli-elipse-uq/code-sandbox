#!/usr/bin/python3

"""
Sandboxes code execution
"""

from base64 import b64encode
from os.path import join
from subprocess import Popen, run, PIPE, TimeoutExpired
from tempfile import TemporaryDirectory
from typing import List
from xvfbwrapper import Xvfb

from codesandbox.typings import Files, TestResult

TIMEOUT = 0.5
ENTRYPOINT = "test.py"
PYTHON_EXEC = "python3"
FIREJAIL_EXEC = "firejail"

def get_firejail_args(tmp_path: str) -> List[str]:
    """ Gets the firejail command to run """

    return [
        FIREJAIL_EXEC,
        "--private={}".format(tmp_path),
        "--quiet",
        PYTHON_EXEC,
        ENTRYPOINT
    ]

def get_x11_firejail_args(tmp_path: str) -> List[str]:
    """ Gets the x11 firejail parameters """

    args = get_firejail_args(tmp_path)

    # Append the x11 flag
    args.append("--x11")

    return args

def write_files(tmp_path: str, files: Files):
    """ Writes a dictionary containing a mapping of filenames to contents
    to the given path
    """

    for filename in files.keys():
        full_path = join(tmp_path, filename)

        with open(full_path, "w") as tmp_file:
            tmp_file.write(files[filename])

def run_code(files: Files) -> TestResult:
    """
    Securely runs code within a sandbox in a temp directory

    The temp directory is automatically removed when the function exits
    """
    with TemporaryDirectory() as tmp:
        write_files(tmp, files)

        args = get_firejail_args(tmp)

        with Popen(args, stdout=PIPE, stderr=PIPE) as proc:
            try:
                proc.wait(TIMEOUT)

                result = TestResult()
                result.stdout = proc.stdout.read().decode()
                result.stderr = proc.stderr.read().decode()
                result.exitCode = proc.returncode

                return result

            except TimeoutExpired:
                proc.terminate()
                proc.wait()

                result = TestResult()
                # TODO: Figure out how to get stdout from this
                result.stdout = ""
                result.stderr = "Code did not finish, possible infinite loop"
                result.exitCode = 1

                return result


def run_gui_code(files: Files):
    """
    Securely runs code within a sandbox in a temp directory

    The temp directory is automatically removed when the function exits
    """
    with TemporaryDirectory() as tmp:

        result = TestResult()
        write_files(tmp, files)

        with Xvfb() as display:
            # Launch the tkinter problem
            display_num = display.new_display
            args = get_x11_firejail_args(tmp)

            with Popen(args, stdout=PIPE, stderr=PIPE) as proc:
                try:
                    proc.wait(TIMEOUT)
                    # Catch syntax errors
                    result = TestResult()
                    result.stdout = proc.stdout.read().decode()
                    result.stderr = proc.stderr.read().decode()
                    result.exitCode = proc.returncode

                    return result

                except TimeoutExpired:
                    # Capture the screen
                    img_path = join(tmp, "output.jpg")
                    run("DISPLAY=:{} import -window root {}"
                        .format(display_num, img_path), shell=True)

                    img_data = ""
                    with open(img_path, "rb") as img:
                        img_data = b64encode(img.read())

                    # Kill the child if it doesn't exit automatically
                    proc.terminate()
                    proc.wait()

                    result.img = img_data.decode()
                    result.stdout = proc.stdout.read().decode()
                    result.stderr = proc.stderr.read().decode()
                    result.exitCode = proc.returncode

    return result
