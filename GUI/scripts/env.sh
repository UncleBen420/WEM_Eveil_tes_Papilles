#!/bin/bash

echo "Starting JSON ENV creation"

PREFIX="VUE_APP_"
OUTPUT="/usr/share/nginx/html/variables.json"



JSON="{"

FIRST_LINE=true

for VAR in $(printenv)
do
    if [[ $VAR == $PREFIX* ]]; then
     	VAR=${VAR#$PREFIX}

        IFS='=' read -r -a array <<< $VAR

        key=${array[0]}

        value=${array[1]}
        if [[ $FIRST_LINE == true ]]; then
            FIRST_LINE=false
        else
            JSON="$JSON,"
        fi    

        JSON=$JSON"\"$key\":\"$value\""
    fi
done
JSON=$JSON"}"

echo "Json generated: $JSON"

touch $OUTPUT
echo $JSON > $OUTPUT


