SHELL := /bin/bash
BASE_PY_EXE := $(shell which python3.10)
IN_VENV = source ".venv/bin/activate"


.PHONY: prep
prep:
	echo "Python: $(BASE_PY_EXE)"
	rm -rf ".venv" || echo "No virtualenv yet"
	$(BASE_PY_EXE) -m venv ".venv"
	pwd && $(IN_VENV) && pip3 install pip-tools
	$(IN_VENV) && pip-sync requirements.txt
	$(IN_VENV) && pip install -e .


.PHONY: sync
sync:
	$(IN_VENV) && pip-sync requirements.txt
	$(IN_VENV) && pip install -e .

.PHONY: refresh-dependencies
refresh-dependencies:
	$(IN_VENV) && pip-compile --verbose --output-file=requirements.txt pyproject.toml

.PHONY: fix
fix:
	$(IN_VENV) && black viya_airtrain
	$(IN_VENV) && ruff --fix --show-fixes viya_airtrain

.PHONY: lint
lint:
	$(IN_VENV) && black --check viya_airtrain
	$(IN_VENV) && ruff --fix viya_airtrain
	$(IN_VENV) && mypy --explicit-package-bases viya_airtrain

