#!/bin/bash

# Do not use "verbose" in order to spot errors easily

# Remove shared resources
rm ./resources/{error,info,question,warning,icon_64x64_cpt}.gif

# Remove other CompareParallelTexts resources
rm ./resources/locale/ru/LC_MESSAGES/CompareParallelTexts.mo

# Remove CompareParallelTexts Python files
rm ./CompareParallelTexts.py

# Remove shared Python files
rm ./{gettext_windows,shared,sharedGUI}.py

# (Linux-only) Remove build scripts
rm ./{build.sh,clean_up.sh,setup.py}

rmdir -p resources/locale/ru/LC_MESSAGES

ls .
