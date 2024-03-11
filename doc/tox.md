# Possible extra: tox

For more elaborate projects, tox can help a lot. Tox is originally a test runner, but it is often used to run (and install) all sorts of project-related tools. The main advantage: it is an automation tool that runs on both linux, mac and windows. Just `pip install tox` and everything else is handled.

`tox.ini` defines what can be run. "What can be run" is called an "environment", so the `-e` in calls like `tox -e coverage` means "select the coverage environment and run it". Anyway, just calling `tox` will normally run the basic actions that github also runs in its checks. So of tox runs OK, github mostly won't complain.

```console
$ tox           # Run all the important bits.
$ tox -e lint   # Run a specific 'environment'
$ tox -qe lint  # -q quiets down the tox output a bit
$ tox list      # List all available 'environments'
$ tox -r        # Rebuild whatever tox cached: cleanup
```

`nens-meta` itself generates the documentation you're now reading by calling `tox -e doc` because there's an extra `[testenv:doc]` at the end of https://github.com/nens/nens-meta/blob/main/tox.ini .

Look at that file for other examples, like checking if the python package builds correctly.
