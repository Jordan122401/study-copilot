PY=python
VENV=.venv

venv:
	$(PY) -m venv $(VENV)

install:
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

ingest:
	$(VENV)/bin/$(PY) scripts/ingest_pdfs.py

index:
	$(VENV)/bin/$(PY) scripts/build_index.py

ask:
	$(VENV)/bin/$(PY) scripts/ask.py "$(Q)"
