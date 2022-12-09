if [ -f .env ]; then
    # Load Environment Variables
    export $(cat .env | grep -v '#' | sed 's/\r$//' | awk '/=/ {print $1}' )
fi

#DIGITAL_OCEAN_API_KEY_CONTAINER_REGISTRY_ENV=$DIGITAL_OCEAN_API_KEY_CONTAINER_REGISTRY
REMOTE_REGISTRY_ENV=DIGITAL_OCEAN_DOCKER_CONTAINER_REGISTRY_NAME

# REF
# https://github.com/python-poetry/poetry/issues/273#issuecomment-982309569

POETRY_NAME_VERSION="$(poetry version)"
PACKAGE_NAME=${POETRY_NAME_VERSION% *}
VERSION=${POETRY_NAME_VERSION#* }

echo "Start Deploying $PACKAGE_NAME:$VERSION"
doctl registry login
docker image tag  "$PACKAGE_NAME:$VERSION" "$REMOTE_REGISTRY_ENV/$PACKAGE_NAME:$VERSION"
docker image push "$REMOTE_REGISTRY_ENV/$PACKAGE_NAME:$VERSION"
