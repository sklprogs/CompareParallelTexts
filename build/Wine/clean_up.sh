#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove shared resources
rm -f ./resources/{error.gif,info.gif,question.gif,warning.gif,icon_64x64_cpt.gif}

# Remove other CompareParallelTexts resources
rm -rf ./locale

# Remove CompareParallelTexts Python files
rm -f ./CompareParallelTexts.py

# Remove shared Python files
rm -f ./{gettext_windows.py,shared.py,sharedGUI.py}

# (Wine-only) Remove CompareParallelTexts icon
rm -f ./resources/icon_64x64_cpt.ico

# (Wine-only) Remove build scripts
rm -f ./{build.sh,clean_up.sh,setup.py,update_cpt.sh}

rmdir resources

ls .