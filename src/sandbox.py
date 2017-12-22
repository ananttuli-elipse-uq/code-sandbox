#!/usr/bin/python3

"""
Sandboxes code execution
"""

from os.path import join
from subprocess import Popen, run, PIPE
from tempfile import TemporaryDirectory
from xvfbwrapper import Xvfb

TIMEOUT = 1
ENTRYPOINT = "test.py"
PYTHON_EXEC = "python3"
FIREJAIL_EXEC = "firejail"

def get_firejail_args(tmp_path):
    """ Gets the firejail command to run """
    return [FIREJAIL_EXEC, "--private={}".format(tmp_path), PYTHON_EXEC, join("~", ENTRYPOINT)]

def write_files(tmp_path, files):
    """ Writes a dictionary containing a mapping of filenames to contents
    to the given path
    """

    for filename in files.keys():
        full_path = join(tmp_path, filename)

        with open(full_path, "w") as tmp_file:
            tmp_file.write(files[filename])

def run_code(files):
    """
    Securely runs code within a sandbox in a temp directory

    The temp directory is automatically removed when the function exits
    """
    with TemporaryDirectory() as tmp:
        write_files(tmp, files)

        args = get_firejail_args(tmp)

        firejail = run(args, stdout=PIPE, stderr=PIPE)
        print(" ".join(args))
        print(firejail.stdout)
        print(firejail.stderr)


def run_gui_code(files):
    """
    Securely runs code within a sandbox in a temp directory

    The temp directory is automatically removed when the function exits
    """
    with TemporaryDirectory() as tmp:


        write_files(tmp, files)
        # Copy files


        script_name = "test.py"

        with Xvfb() as display:
            # Launch the tkinter problem
            args = "python3 " + script_name
            with Popen(args, shell=True, executable="/bin/bash", stdout=PIPE, stderr=PIPE) as p:
                try:
                    p.wait(TIMEOUT)
                    print("Process exited before screen capture")
                except Exception as e:
                    # Capture the screen
                    display_num = display.new_display
                    print("Capturing...")
                    run("DISPLAY=:{} import -window root ~/test.png"
                        .format(display_num), shell=True)

                    # Kill the child if it doesn't exit automaticallyj
                    p.kill()


if __name__ == "__main__":
    FILES = {
        "test.py": "print('Hello world')"
    }

    run_code(FILES)
