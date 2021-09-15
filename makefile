SHELL := /bin/bash
.PHONY: all clean install test 

help: 	    ## Show this help.
	@echo "Please use \`make <target>' where <target> is one of"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: install test 

test:       ## Run project tests
	pytest

cov:   		## Run project tests
	pytest --cov-report term-missing --cov=gallery

create_env: ## Create Virtual Env.
	python3 -m venv venv

install:    ## Run project tests
	pip install --upgrade pip
	pip install -r requirements/dev.txt

run:        ## Run the project
	flask run

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build