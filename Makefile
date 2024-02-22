#!make
VERSION := $(shell cat src/build_ver)
export VERSION
unexport CONDA_PREFIX  # if conda is installed, it will mess with the virtual env

.HELP: version ## Show the current version
version:
	echo ${VERSION}

.HELP: reqs  ## Upgrade requirements including pre-commit
reqs:
	pre-commit autoupdate
	bash ./scripts/compile_requirements.sh
	uv pip install -r requirements.dev.txt

.HELP: test  ## Run tests (you can use -k or -m to filter them by name or by mark respectively)
test:
	scripts/test.sh

.HELP: run  ## Run the application
run:
	scripts/run_dev.sh

.HELP: codegen  ## Generate code Generates python code from Open API
codegen:
	scripts/codegen.sh

.HELP: create-keys  ## Recreates key and certificate at security folder
create-keys:
	scripts/create_keys.sh

.HELP: db-migration  ## Create migration script in alembic/versions/
db-migration:
	scripts/db_migration.sh

.HELP: db-show-migration  ## Show migration script as SQL
db-show-migration:
	scripts/db_show_migration_sql.sh

.HELP: db-upgrade  ## Run migrations from alembic/versions/
db-upgrade:
	scripts/db_upgrade.sh

.HELP: dev  ## Run backend on local Python in Linux
dev:
	scripts/dev.sh

.HELP: load  ## Run load tests (URL in load.yaml)
load:
	scripts/load.sh

.HELP: markup  ## Convert Swagger API into Confluence Wiki compatible markdown
markup:
	scripts/markup.sh

.HELP: prod  ## Run backend on AWS
prod:
	scripts/prod.sh

.HELP: psql  ## Run PostgreSQL CLI
psql:
	scripts/psql.sh

.HELP: smoke-test  ## Quick curl test (request JWT and after that user list with it)
smoke-test:
	scripts/smoke_test.sh

.HELP: git-hook-install  ## Install git hook to add 'build' date to application
git-hook-install:
	scripts/git_hook_install.sh

.HELP: help  ## Display this message
help:
	@grep -E \
		'^.HELP: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".HELP: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
