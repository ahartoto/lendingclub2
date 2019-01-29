# Filename: Makefile

PYTHON := python3
PYLINT := pylint
PYTEST := pytest

PKG := lendingclub2

lint:
	@$(PYLINT) $(PKG)

test:
	@PYTHONPATH=$(PWD) $(PYTEST) tests

package:
	@$(PYTHON) setup.py bdist_wheel
