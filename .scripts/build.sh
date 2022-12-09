# REF
# https://github.com/python-poetry/poetry/issues/273#issuecomment-982309569

POETRY_NAME_VERSION="$(poetry version)"
PACKAGE_NAME=${POETRY_NAME_VERSION% *}
VERSION=${POETRY_NAME_VERSION#* }

echo "Start building $PACKAGE_NAME:$VERSION"
docker build ./ -t "$PACKAGE_NAME:$VERSION"
