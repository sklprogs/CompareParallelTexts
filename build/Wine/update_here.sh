#!/bin/sh

# Do not use "verbose" in order to spot errors easily

mkdir ./resources

# Copy shared resources
cp -u /usr/local/bin/shared/resources/{error.gif,info.gif,question.gif,warning.gif,icon_64x64_cpt.gif} ./resources/

# Copy other CompareParallelTexts resources
cp -ru /usr/local/bin/CompareParallelTexts/locale .

# Copy CompareParallelTexts Python files
cp -u /usr/local/bin/CompareParallelTexts/CompareParallelTexts.py .

# Copy shared Python files
cp -u /usr/local/bin/shared/{gettext_windows.py,shared.py,sharedGUI.py} .

# (Wine-only) Copy CompareParallelTexts icon
cp -ru /home/pete/bin/CompareParallelTexts/resources/icon_64x64_cpt.ico ./resources/

# (Wine-only) Copy build scripts
cp -u /usr/local/bin/CompareParallelTexts/build/Wine/{build.sh,clean_up.sh,setup.py,update_cpt.sh} .

ls .
