# Code Sandbox

> Allows sandboxed execution of code

NOTE: Firejail does not work correctly on EAIT infrastructure,
due to virtualization issues. For the time being this can be run on
any other cloud hosting platform.


## Requirements

- Python 3.6 (`apt install python3 python3-pip`)
- Firejail (`apt install firejail`)
- Xvfb (`apt install xvfb`)
- ImageMagick (`apt install imagemagick`)

## Installation

```
$ pip3 install -r requirements.txt
```

## Running

The included Makefile has the following targets:

- `test`: Run tests
- `lint`: Runs the linter

## Verifying the sandboxing is working

To verify that firejail and other components are installed correctly, run:

```bash
$ make test
```
