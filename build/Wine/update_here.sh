#!/bin/sh

# Do not use "verbose" in order to spot errors easily

mkdir -p ./resources/locale/ru/LC_MESSAGES/

# Copy shared resources
cp -u /usr/local/bin/shared/resources/{error.gif,info.gif,question.gif,warning.gif,icon_64x64_cpt.gif} ./resources/

# Copy other CompareParallelTexts resources
cp -u /usr/local/bin/CompareParallelTexts/resources/locale/ru/LC_MESSAGES/CompareParallelTexts.mo ./resources/locale/ru/LC_MESSAGES/

# Copy CompareParallelTexts Python files
cp -u /usr/local/bin/CompareParallelTexts/src/CompareParallelTexts.py .

# Copy shared Python files
cp -u /usr/local/bin/shared/src/{gettext_windows.py,shared.py,sharedGUI.py} .

# (Wine-only) Copy CompareParallelTexts icon
cp -ru /home/pete/bin/CompareParallelTexts/resources/icon_64x64_cpt.ico ./resources/

# (Wine-only) Copy build scripts
cp -u /usr/local/bin/CompareParallelTexts/build/Wine/{build.sh,clean_up.sh,CompareParallelTexts.cmd,setup.py,update_cpt.sh} .

ls .
