#!/usr/bin/env bash
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

OUT=swagger-codegen
mkdir -p $OUT
docker run --rm -it -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/$IN -g python-flask -o /local/$OUT
echo "...yaml..."
cp $OUT/openapi_server/openapi/openapi.yaml src/openapi_server/openapi
echo "...models..."
cp -r $OUT/openapi_server/models src/openapi_server/
echo "...root units..."
cp $OUT/openapi_server/*.* src/openapi_server/
git add src/openapi_server/\*.*
rm -r $OUT/.openapi-generator
find $OUT/ -type f -maxdepth 1 -exec rm {} \;
rm -r $OUT/openapi_server/models
rm -r $OUT/openapi_server/openapi
rm -r $OUT/openapi_server/test
find $OUT/openapi_server/ -type f -maxdepth 1 -exec rm {} \;

echo
echo "Python code from Open API (swagger) description generated in swagger/"
echo
