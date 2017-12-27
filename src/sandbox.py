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

def get_x11_firejail_args(tmp_path: str, display_num: int) -> List[str]:
    """ Gets the x11 firejail parameters """

    args = [
        # "DISPLAY=:{}".format(display_num)
    ]

    args.extend(get_firejail_args(tmp_path))

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
            display_num = display.new_display
            args = get_x11_firejail_args(tmp, display_num)
            print(" ".join(args))
            with Popen(args, stdout=PIPE, stderr=PIPE) as proc:
                try:
                    proc.wait(TIMEOUT)
                    raise RuntimeError("Process exited before screen capture")
                except TimeoutExpired:
                    # Capture the screen
                    print("Capturing...")
                    run("DISPLAY=:{} import -window root ~/test.png"
                        .format(display_num), shell=True)

                    # Kill the child if it doesn't exit automatically
                    proc.kill()


if __name__ == "__main__":

    contents = ""
    with open("test_scripts/sample_gui.py", "r") as f:
        contents = f.read()

    FILES = {
        "test.py": contents,
    }

    print(run_gui_code(FILES))
