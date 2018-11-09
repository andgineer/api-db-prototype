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
docker run --rm -it -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i /local/$IN -l python-flask -o /local/$OUT
cp $OUT/swagger_server/swagger/swagger.yaml src/swagger_server/swagger
echo
echo "Python code from Open API (swagger) description generated in swagger/"
echo
