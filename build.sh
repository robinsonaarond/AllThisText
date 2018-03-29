#! /bin/bash

# Requires pyinstaller
# To install:  pip install pyinstaller

rm -rf build dist AllThisText.spec
pyinstaller --onefile AllThisText.py
cp dist/AllThisText .
rm -rf build dist AllThisText.spec
