#!/bin/bash

VERSION=$(cat VERSION)

NAME="Agent_Memory_Vault_v${VERSION}"

echo "Building ${NAME}..."

mkdir -p releases

rm -rf /tmp/${NAME}

mkdir /tmp/${NAME}

rsync -av --exclude='__pycache__' --exclude='*.pyc' agent_memory /tmp/${NAME}/

rsync -av --exclude='__pycache__' --exclude='*.pyc' examples /tmp/${NAME}/
cp -r docs /tmp/${NAME}/

cp README.md /tmp/${NAME}/
cp LICENSE /tmp/${NAME}/
cp CHANGELOG.md /tmp/${NAME}/
cp VERSION /tmp/${NAME}/
cp pyproject.toml /tmp/${NAME}/


cd /tmp

zip -r "${OLDPWD}/releases/${NAME}.zip" "${NAME}"


echo ""
echo "Release created:"
echo "${OLDPWD}/releases/${NAME}.zip"
