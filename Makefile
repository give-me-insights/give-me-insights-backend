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
	@git add poetry.toml
	@git commit -m "patch version"
	@bash .scripts/create-version-tag.sh
