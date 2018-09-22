#!/bin/bash

# Do not use "verbose" in order to spot errors easily

mkdir -p ./resources/locale/ru/LC_MESSAGES/

# Copy shared resources
cp -u $HOME/bin/shared/resources/{error,info,question,warning,icon_64x64_cpt}.gif ./resources/

# Copy other CompareParallelTexts resources
cp -u $HOME/bin/CompareParallelTexts/resources/locale/ru/LC_MESSAGES/CompareParallelTexts.mo ./resources/locale/ru/LC_MESSAGES/

# Copy CompareParallelTexts Python files
cp -u $HOME/bin/CompareParallelTexts/src/CompareParallelTexts.py .

# Copy shared Python files
cp -u $HOME/bin/shared/src/{gettext_windows,shared,sharedGUI}.py .

# (Linux-only) Copy build scripts
cp -u $HOME/bin/CompareParallelTexts/build/Linux/{build.sh,clean_up.sh,setup.py} .

ls .
