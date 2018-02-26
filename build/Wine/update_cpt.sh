#!/bin/sh

./update_here.sh
./build.sh
cp $HOME/tmp/ars/CompareParallelTexts.7z .
7z x CompareParallelTexts.7z
rm CompareParallelTexts.7z
cp -ru build/exe.win32-3.4/* CompareParallelTexts/
cp -ru locale resources CompareParallelTexts/
cd CompareParallelTexts && wine CompareParallelTexts.exe
read -p "Update the archive? (y/n) " choice
cd ..
if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
	7z a CompareParallelTexts.7z CompareParallelTexts/ && rm -r build CompareParallelTexts
	mv -fv $HOME/tmp/ars/CompareParallelTexts.7z $HOME/tmp/ars/CompareParallelTexts\ \(OLD\).7z
	mv -v ./CompareParallelTexts.7z $HOME/tmp/ars/CompareParallelTexts.7z
fi
./clean_up.sh
