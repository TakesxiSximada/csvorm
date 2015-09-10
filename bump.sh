#! /usr/bin/env sh
# -*- coding: utf-8 -*-
VERSION_FILE=src/csvorm/version.txt
part="$1"
if [ "$part" = "" ]
then
    echo "need part!!"
    exit 1
fi

old_version=`cat $VERSION_FILE`
bumpversion --current-version $old_version $part --allow-dirty
new_version=`cat $VERSION_FILE`
echo $old_version "->" $new_version
