#!/bin/bash

function error () {
    echo "Error: $1"
    exit 1
}

cd "../EscoHelperLib"                               || error "Changing to lib directory"
npx webpack-cli --mode production --target node     || error "Generating optimized production version for NodeJS"
cp dist/esco-helper.js ../EscoHelperApi/lib/        || error "Copying generated library to lib directory"

echo -ne "\n\n >>> Library was Synchorized Succesfully at lib/\n\n"