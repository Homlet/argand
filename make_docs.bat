@echo off
setlocal

pushd src
..\docs\doxygen\doxygen ..\docs\argand.cfg
popd

pause
