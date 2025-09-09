#!/bin/bash
uv run src/nens_meta/nens_toml.py
uv run src/nens_meta/pyproject_toml.py
uv run --group docs sphinx-build doc doc/_build --color -b html
