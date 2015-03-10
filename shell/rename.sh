#!/bin/bash

# we have less than 3 arguments. Print the help text:
if [[ $# -lt 2 ]] ; then
cat << HELP
$0 -- renames a number of files using sed regular expressions USAGE: ren 'regexp' 'replacement' files...
EXAMPLE: $0 file1 file2
HELP
exit 0
fi
OLD="$1"
NEW="$2"
# The shift command removes one argument from the list of
# command line arguments.
shift
shift

if [[ -f "$OLD" ]] ; then
   newfile=`echo "$OLD" | sed "s/${OLD}/${NEW}/g"`
   if [[ -f "$NEW" ]]; then
　　　　   echo "ERROR: $NEW exists already"
   else
      echo "renaming $OLD to $NEW ..."
      mv "$OLD" "$NEW"
      if [[ "$?" -eq 0 ]]; then
         echo OK
      fi
   fi
else
   echo "ERROR: $OLD is not exsit!"
fi