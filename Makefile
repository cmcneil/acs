SHELL := /bin/bash
ENV := $(PWD)/.env
# Include environment variables from .env file, if it exists
# https://dev.to/serhatteker/get-environment-variables-from-a-file-into-makefile-2m5l
-include $(ENV)
# Export the UV_INDEX_FOREST_USERNAME variable to subprocesses
export UV_INDEX_FOREST_USERNAME

.PHONY: token-exists
token-exists: ## Checks if required Gemfury token exists in environment
	@if [ -z "${UV_INDEX_FOREST_USERNAME}" ]; then \
		echo "🚨 Gemfury Forest-index token needed for uv/pip and not found in environment."; \
		echo "Please set the UV_INDEX_FOREST_USERNAME environment variable with your deploy token."; \
		echo "You can get the token from https://manage.fury.io/manage/forest-neurotech/tokens/pull"; \
		exit 1; \
	fi

.PHONY: install
install: install-python-dep

.PHONY: install-dev
install-dev: install-python-dep-dev

.PHONY: install-python-dep
install-python-dep: token-exists ## Installs Python dependencies using uv with frozen requirements
	@echo "🚀 Installing dependencies"
	@uv sync --frozen --extra complete

.PHONY: install-python-dep-dev
install-python-dep-dev: token-exists ## Installs development Python dependencies
	@echo "🚀 Installing development dependencies"
ifeq ($(shell uname -s),Darwin)
	@uv sync --extra dev --python-preference only-managed
else
	@uv sync --extra dev
endif

.PHONY: check
check: token-exists ## Run code quality tools.
#	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
#	@uv sync --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running pyright"
	@uv run --no-sync pyright --warnings
	@echo "🚀 Spell checking"
	uv run --no-sync codespell src --ignore-words=resources/dictionary.txt --skip="docs/build/**/*"


.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@ENV_FOR_DYNACONF=test uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: dev
dev: ## Run the development server
	@echo "Running Dagster local server"
	@uv run dagster dev -w workspace.yaml

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"


.PHONY: docs
docs: install-dev ## Builds documentation
	@echo "🚀 Building documentation"
	@make -C docs html


.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
