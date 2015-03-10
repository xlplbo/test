#!/bin/bash

a="hello world" #not have any spaces
echo "A is: " $a
echo "B is: ${a}!"

#let
var=1
let "var+=1"
echo $var

#if []; then elif []; then else fi
if [[ -f "test.sh" ]]; then
	echo "test.sh is exsit!"
else
	echo "test.sh is not exsit!"
fi

if [[ -x "/bin/ls" ]]; then
	/bin/ls
elif [[ -n "$var" ]]; then
	echo $var
elif [[ "$a" = "$var" ]]; then
	echo "a = var"
else
	echo "nothing"
fi

if [[ ${SHELL} = "/bin/bash" ]]; then
	echo "bash"
else
	echo "no bash"
fi

#&& and ||
mailfolder=/var/spool/mail/liubo5
[[ -r "$mailfolder" ]] || { echo "can not read $mailfolder"; }
echo "$mailfolder has mail:"
grep "^From " $mailfolder

[[ -f "/etc/shadow" ]] && echo "This computer uses shadow passwords"

#case
ftpye="$(file "$1")"
case "$ftpye" in
	"$1: Zip archive")
		unzip "$1" ;;
	"$1: gZip compressed")
		gunzip "$1" ;;
	"$1: bzip2 compressed")
		bunzip2 "$1" ;;
	*)
	echo "File $1 can not be uncompressed!" ;;
esac

#select
echo "what is your favourite OS?"
select var in "Linux" "Free BSD" "Mac OS" "Windows"; do
	break;
done
echo "You have selcted $var"

#while/for
for (( i = 0; i < 10; i++ )); do
	echo "i = $i"
done

for var in A B C; do
	echo "var is $var"
done

# list a content summary of a number of RPM packages
# USEAGE: showrpm rpmfile1 rpmfile2 ...
# e.g.: showrpm /cdrom/Rethat/RPMS/*.rpm
for rpmpackage in "$@"; do
	if [[ -r "$rpmpackage" ]]; then
		rpm -qi -p $rpmpackage
	else
		echo "ERROR: cannot read file $rpmpackage"
	fi
done

echo $SHELL
echo "$SHELL"
echo '$SHELL'
echo \$SHELL
