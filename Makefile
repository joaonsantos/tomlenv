Q=@
POETRY                := poetry
POETRY_INSTALL_FLAGS  := --no-root --sync

.PHONY: dev
dev:
	$Q$(POETRY) install $(POETRY_INSTALL_FLAGS)

ISORT_CMD  := isort .
BLACK_CMD  := black .
.PHONY: fmt
fmt:
	$Q$(POETRY) run $(ISORT_CMD)
	$Q$(POETRY) run $(BLACK_CMD)

PYTHON := python

.PHONY: test
test:
	$Q$(POETRY) run $(COVERAGE) run -m unittest discover tests

COVERAGE := coverage

.PHONY: cov
cov: test
	$Q$(POETRY) run $(COVERAGE) report