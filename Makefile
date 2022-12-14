help:

build_and_deploy:
	@bash .scripts/build.sh
	@bash .scripts/deploy.sh

patch_version_build_and_deploy:
	@bash .scripts/patch_version.sh
	@bash .scripts/build.sh
	@bash .scripts/deploy.sh

patch_version_push_tag:
	@bash .scripts/patch_version.sh
	@git add pyproject.toml
	@git commit -m "patch version"
	@bash .scripts/create-version-tag.sh


push_tag:
	@bash .scripts/create-version-tag.sh

initial_migration:
	@bash poetry run python app/manage.py migrate
	@bash poetry run python app/manage.py loaddata company.json
