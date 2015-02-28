@echo off
setlocal

pushd src
python ..\build\setup.py -q build
popd

copy docs\pdf\Argand_Plotter_Manual_en-uk.pdf build\Win32GUI\Argand_Plotter_Manual_en-uk.pdf
