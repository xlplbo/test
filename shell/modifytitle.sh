#!/bin/bash

help()
{
cat << HELP
	$0 -- change the name of an xterm, gnome-terminal or kde konsole
	USAGE: $0 [-h] "string_for_titelbar"
	OPTIONS: -h help text
	EXAMPLE: $0 "cvs"
HELP
	exit 0
}
# in case of error or if -h is given we call the function help:
[[ -z "$1" ]] && help
[[ "$1" = "-h" ]] && help
# send the escape sequence to change the xterm titelbar:
echo -e "\033]0;$1\007"
