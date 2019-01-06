#!/usr/bin/env bash

OUT=swagger-codegen
SRV=src/openapi_server

if [ -n "$1" ] && [[ "$1" =~ ^[^\-].* ]]; then
    IN=$1
else
    IN=api/swagger.yaml
fi

echo
echo "Generates python code from Open API (swager) description"
echo "codegen.sh <yaml_or_json_file>"
echo "by default api/swagger.yaml"
echo
echo "Modify $SRV/controllers by yourself based on generated ones in $OUT/controllers"


# Generate Python's clients
mkdir -p $OUT
docker run --rm -it -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/$IN -g python-flask -o /local/$OUT

# Copy to our source excluding controllers
echo "...yaml..."
cp $OUT/openapi_server/openapi/openapi.yaml $SRV/openapi
echo "...models..."
cp -r $OUT/openapi_server/models $SRV
echo "...root units..."
cp $OUT/openapi_server/*.* $SRV/
git add $SRV/\*.*

# Cleaning up
rm -r $OUT/.openapi-generator
find $OUT/ -type f -maxdepth 1 -exec rm {} \;
rm -r $OUT/openapi_server/models
rm -r $OUT/openapi_server/openapi
rm -r $OUT/openapi_server/test
find $OUT/openapi_server/ -type f -maxdepth 1 -exec rm {} \;

echo
echo "Controllers generated from Open API (swagger) description are in $OUT, units copyed to $SRV"
echo
