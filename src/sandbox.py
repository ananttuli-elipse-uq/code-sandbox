#!/usr/bin/python3

"""
Sandboxes code execution
"""

from os.path import join
from subprocess import Popen, run, PIPE, TimeoutExpired
from tempfile import TemporaryDirectory
from typing import List
from xvfbwrapper import Xvfb
from typings import Files, TestResult

TIMEOUT = 1
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
        join(tmp_path, ENTRYPOINT)
    ]

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

        firejail = run(args, stdout=PIPE, stderr=PIPE)

    result = TestResult()
    result.stdout = firejail.stdout.decode()
    result.stderr = firejail.stderr.decode()
    result.exitCode = firejail.returncode

    return result



def run_gui_code(files: Files):
    """
    Securely runs code within a sandbox in a temp directory

    The temp directory is automatically removed when the function exits
    """
    with TemporaryDirectory() as tmp:

        write_files(tmp, files)

        with Xvfb() as display:
            # Launch the tkinter problem
            args = get_firejail_args(tmp)
            with Popen(args, stdout=PIPE, stderr=PIPE) as proc:
                try:
                    proc.wait(TIMEOUT)
                    print("Process exited before screen capture")
                except TimeoutExpired:
                    # Capture the screen
                    display_num = display.new_display
                    print("Capturing...")
                    run("DISPLAY=:{} import -window root ~/test.png"
                        .format(display_num), shell=True)

                    # Kill the child if it doesn't exit automaticallyj
                    proc.kill()


if __name__ == "__main__":
    FILES = {
        "test.py": "import file2\nprint('Hello world')",
        "file2.py": "print('Loaded file 2')"
    }

    print(run_code(FILES))
