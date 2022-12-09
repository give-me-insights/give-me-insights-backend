help:

build_and_deploy:
	@bash .scripts/build.sh
	@bash .scripts/deploy.sh

patch_version_build_and_deploy:
	@bash .scripts/patch_version.sh
	@bash .scripts/build.sh
	@bash .scripts/deploy.sh
