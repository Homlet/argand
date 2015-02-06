@echo off
setlocal

pushd src
python ..\build\setup.py -q build
popd
