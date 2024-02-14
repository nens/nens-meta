# Generic development instructions/tips for working on this kind of project

This project mostly uses the generic "nens-meta" setup. The idea:

- Use a virtualenv in a standard location and activate it.
- The tricky bits are pre-configured (vscode, pytest, formatting, etc).
- VScode should work out of the box.
- Commandline usage too.

(Note: this documentation was generated automatically.)

## Python virtualenv

Virtualenvs keep your global python installation nice and clean. They also help code completion.

- Create the virtualenv in the `venv` dir. This is a convention that's also picked up by vscode
- Activate it when working on the project.
- Install the requirements.

    $ python3 -m venv venv --prompt nens-meta
    $ venv/bin/activate
    $ pip install -r requirements.txt

On mac/linux the activate step is slightly different:

    $ source venv/bin/activate
