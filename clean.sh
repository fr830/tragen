#!/bin/bash

rec_clean() {
	for file in $(ls $1 | grep .swp); do rm "$1/$file" 2>/dev/null; done
	for file in $(ls $1 | grep .pyc); do rm "$1/$file" 2>/dev/null; done
	for el in $(ls $1)
	do
		if [ -d "$1/$el" ]
		then
			rec_clean "$1/$el"
		fi
	done
}


rec_clean $1
