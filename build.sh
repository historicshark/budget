#! /usr/bin/env bash

rm -rf build dist
pyinstaller --windowed --name "BudgetProgram" --icon=icon.icns --add-data=assets:assets main.py
cp -r dist/BudgetProgram.app /Applications
rm -rf build dist
