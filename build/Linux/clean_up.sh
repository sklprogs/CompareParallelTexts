#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove shared resources
rm -f ./resources/{error.gif,info.gif,question.gif,warning.gif,icon_64x64_cpt.gif}

# Remove other CompareParallelTexts resources
rm -f ./resources/locale/ru/LC_MESSAGES/CompareParallelTexts.mo

# Remove CompareParallelTexts Python files
rm -f ./CompareParallelTexts.py

# Remove shared Python files
rm -f ./{gettext_windows.py,shared.py,sharedGUI.py}

# (Linux-only) Remove build scripts
rm -f ./{build.sh,clean_up.sh,setup.py}

rmdir -p resources/locale/ru/LC_MESSAGES

ls .
