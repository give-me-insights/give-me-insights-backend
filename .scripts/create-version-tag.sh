POETRY_NAME_VERSION="$(poetry version)"
VERSION=${POETRY_NAME_VERSION#* }

git tag -a "v$VERSION" -m "version $VERSION"
git push origin "v$VERSION"
