#!/bin/bash

# Do not use "verbose" in order to spot errors easily

# Remove shared resources
rm -f ./resources/{error,info,question,warning,icon_64x64_cpt}.gif

# Remove other CompareParallelTexts resources
rm -f ./resources/locale/ru/LC_MESSAGES/CompareParallelTexts.mo

# Remove CompareParallelTexts Python files
rm -f ./CompareParallelTexts.py

# Remove shared Python files
rm -f ./{gettext_windows,shared,sharedGUI}.py

# (Wine-only) Remove CompareParallelTexts icon
rm -f ./resources/icon_64x64_cpt.ico

# (Wine-only) Remove build scripts
rm -f ./{build.sh,clean_up.sh,CompareParallelTexts.cmd,setup.py,update_cpt.sh}

rmdir -p resources/locale/ru/LC_MESSAGES

ls .
