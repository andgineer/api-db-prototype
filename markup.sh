#!/usr/bin/env bash
CONVERTER=swagger2markup-cli.jar
REPO=https://oss.jfrog.org/artifactory/oss-snapshot-local/io/github/swagger2markup/swagger2markup-cli/1.3.1-SNAPSHOT/swagger2markup-cli-1.3.1-20170317.083338-3.jar
if [ ! -f $CONVERTER ]; then
    echo
    echo "No coverter was found locally, downloading..."
    echo
    wget -O $CONVERTER $REPO
fi
# download the converter from
# https://oss.jfrog.org/artifactory/oss-snapshot-local/io/github/swagger2markup/swagger2markup-cli/1.3.1-SNAPSHOT/
rm -r --force api/markup
java -jar $CONVERTER convert --outputFile api/markup/swagger --swaggerInput api/swagger.yaml --config markup.cfg
