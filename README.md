# Code Sandbox

> Allows sandboxed execution of code behind a REST api

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

## Environment Setup

Copy `.env.example` to `.env` and set the API key,
this API key goes into the json payload when making requests

## Running

The included Makefile has the following targets:

- `test`: Run tests
- `lint`: Runs the linter
- `dev`: Runs the Flask development server on port 5000

## Verifying the sandboxing is working

To verify that firejail and other components are installed correctly, run:

```bash
$ make test
```

## Deploying

### Running gunicorn
```
$ gunicorn -w 4 --bind 0.0.0.0:8000 codesandbox:app
```

### Deploying with Supervisor
```
$ apt install supervisor
# Modify codesandbox.conf to contain the correct values for project directory
$ cp codesandbox.conf /etc/supervisor/conf.d/codesandbox.conf
$ supervisorctl reread
$ supervisorctl update
```

## Endpoints

<table>
    <tr>
        <td><code>/run</code></td>
        <td>POST</td>
        <td>Executes and returns the result of provided code</td>
    </tr>
</table>
