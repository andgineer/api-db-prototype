#!make
VERSION := $(shell cat src/build_timestamp)
export VERSION

version:
	echo ${VERSION}

ver-bug:
	bash ./scripts/verup.sh bug

ver-feature:
	bash ./scripts/verup.sh feature

ver-release:
	bash ./scripts/verup.sh release

reqs:
	pre-commit autoupdate
	bash ./scripts/compile_requirements.sh
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

test:
	scripts/test.sh

run:
	scripts/run_dev.sh

upgrade: reqs
	scripts/upgrade.sh
