#!/usr/bin/env bash
#
# Converts swagger API into confluence wiki compatible markdown
#
echo
echo "swagger2markup do not support swagger 3: https://github.com/Swagger2Markup/swagger2markup/issues/340"
echo "so to convert our OpenAPI 3 spec back to swagger 2 we use https://github.com/juan-lb/openapi2swagger."
echo "After that we convert this swagger 2 spec to markup."
echo
echo "Resulting markup will be in api/markup/swagger.txt"
echo "content of this file you can insert to Atlassian Confluence page:"
echo "open submenu in big plus(+) sign on top-right and select 'Markup', insert swagger.txt content."
echo
SPEC2="api/swagger2.json"
CONVERTER=swagger2markup-cli.jar
REPO=https://oss.jfrog.org/artifactory/oss-snapshot-local/io/github/swagger2markup/swagger2markup-cli/1.3.1-SNAPSHOT/swagger2markup-cli-1.3.1-20170317.083338-3.jar
docker run -v $PWD/api:/tmp -e OPENAPI_FILE=swagger.yaml  openapi2swagger:latest > $SPEC2
if [[ $? != 0 ]]; then
    echo "You should create openapi2swagger container as described on https://github.com/juan-lb/openapi2swagger"
    exit 1
fi
if [ ! -f $CONVERTER ]; then
    echo
    echo "No coverter was found locally, downloading..."
    echo
    wget -O $CONVERTER $REPO
fi
rm -r --force api/markup
java -jar $CONVERTER convert --outputFile api/markup/swagger --swaggerInput $SPEC2 --config markup.cfg
